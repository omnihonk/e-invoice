import os
import subprocess
import tempfile
import urllib.request
import xml.etree.ElementTree as ET

# Default properties
MUSTANG_VERSION = "2.23.0"
MUSTANG_JAR_URL = f"https://repo1.maven.org/maven2/org/mustangproject/Mustang-CLI/{MUSTANG_VERSION}/Mustang-CLI-{MUSTANG_VERSION}.jar"

def get_mustang_jar_path() -> str:
    """Determine and ensure availability of Mustang-CLI jar."""
    # 1. Check environment variable
    env_path = os.getenv("MUSTANG_CLI_JAR")
    if env_path and os.path.exists(env_path):
        return env_path
    
    # 2. Check standard docker container path
    docker_path = f"/app/Mustang-CLI-{MUSTANG_VERSION}.jar"
    if os.path.exists(docker_path):
        return docker_path
    
    # 3. Check local data directory path
    local_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(local_data_dir, exist_ok=True)
    local_path = os.path.join(local_data_dir, f"Mustang-CLI-{MUSTANG_VERSION}.jar")
    
    if os.path.exists(local_path):
        return local_path
    
    # 4. Proactive automatic download for local dev / non-docker environments
    try:
        print(f"Downloading Mustang-CLI-{MUSTANG_VERSION}.jar from Maven Central...")
        urllib.request.urlretrieve(MUSTANG_JAR_URL, local_path)
        print("Download completed successfully.")
        return local_path
    except Exception as e:
        # If download fails, check if any generic Mustang jar is in local_data_dir
        for file in os.listdir(local_data_dir):
            if file.startswith("Mustang-CLI") and file.endswith(".jar"):
                return os.path.join(local_data_dir, file)
        raise RuntimeError(f"Mustang-CLI jar not found and download failed: {str(e)}")

def parse_mustang_xml(xml_str: str) -> dict:
    """Parse Mustang validator XML output into a clean structured dictionary."""
    try:
        # Strip any leading logs or non-xml output
        start_idx = xml_str.find("<?xml")
        if start_idx == -1:
            start_idx = xml_str.find("<validation")
        if start_idx != -1:
            xml_str = xml_str[start_idx:]
            
        root = ET.fromstring(xml_str.strip())
        
        # Determine overall validity
        xml_node = root.find("xml")
        pdf_node = root.find("pdf")
        
        xml_status = "unknown"
        pdf_compliant = True
        
        info = {}
        errors = []
        
        # 1. Parse XML block
        if xml_node is not None:
            xml_summary = xml_node.find("summary")
            if xml_summary is not None:
                xml_status = xml_summary.get("status", "unknown")
                
            xml_info = xml_node.find("info")
            if xml_info is not None:
                for child in xml_info:
                    if child.tag == "rules":
                        fired = child.find("fired")
                        failed = child.find("failed")
                        info["rules"] = {
                            "fired": int(fired.text or 0) if fired is not None else 0,
                            "failed": int(failed.text or 0) if failed is not None else 0
                        }
                    elif child.tag == "duration":
                        info["duration_ms"] = int(child.text or 0)
                    else:
                        info[child.tag] = child.text
                        
            # Extract failed assertions from XML validation if any
            for error_node in xml_node.findall(".//error"):
                text = error_node.text
                if text and text.strip():
                    errors.append(f"XML: {text.strip()}")
        else:
            # Fallback if no separate xml block exists
            summary_el = root.find("summary")
            if summary_el is not None:
                xml_status = summary_el.get("status", "unknown")
            
            info_el = root.find("info")
            if info_el is not None:
                for child in info_el:
                    if child.tag == "rules":
                        fired = child.find("fired")
                        failed = child.find("failed")
                        info["rules"] = {
                            "fired": int(fired.text or 0) if fired is not None else 0,
                            "failed": int(failed.text or 0) if failed is not None else 0
                        }
                    elif child.tag == "duration":
                        info["duration_ms"] = int(child.text or 0)
                    else:
                        info[child.tag] = child.text
                        
        # 2. Parse PDF block if present
        if pdf_node is not None:
            is_compliant_str = pdf_node.get("isCompliant", "true")
            pdf_compliant = (is_compliant_str.lower() == "true")
            
            # Extract PDF compliance warnings if present
            pdf_errors = []
            for error_node in pdf_node.findall(".//error"):
                text = error_node.text
                if text and text.strip():
                    pdf_errors.append(text.strip())
            
            # Since standard local PDF generators lack custom output intent color profiles
            # we keep PDF errors as visual compliance warnings but focus validation on e-invoice XML data.
            if not pdf_compliant and pdf_errors:
                info["pdf_compliance_warnings"] = pdf_errors[:10] # limit to 10 warnings
                
        is_valid = (xml_status == "valid")
        
        # Generic fallback
        if not is_valid and not errors:
            for el in root.iter():
                if "error" in el.tag.lower() or "fail" in el.tag.lower():
                    if el.text and el.text.strip():
                        errors.append(f"{el.tag}: {el.text.strip()}")
            if not errors:
                errors.append("XML schema validation failed.")
                
        return {
            "is_valid": is_valid,
            "status": xml_status,
            "pdf_compliant": pdf_compliant,
            "info": info,
            "errors": errors,
            "raw_xml": xml_str
        }
    except Exception as e:
        return {
            "is_valid": False,
            "status": "error",
            "pdf_compliant": False,
            "info": {},
            "errors": [f"Failed to parse Mustang validation XML: {str(e)}"],
            "raw_xml": xml_str
        }


def validate_pdf_bytes(pdf_bytes: bytes) -> dict:
    """Validate Factur-X PDF bytes against Mustangproject validator CLI."""
    jar_path = get_mustang_jar_path()
    
    # Save the PDF to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
        tmp_file.write(pdf_bytes)
        tmp_path = tmp_file.name
        
    try:
        # Run Mustang CLI validate action
        result = subprocess.run(
            ["java", "-jar", jar_path, "--action", "validate", "--no-notices", "--source", tmp_path],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Capturing stdout as main validation report source
        report_data = result.stdout or ""
        stderr_data = result.stderr or ""
        
        # If there is no XML in stdout, but exit code is non-zero, capture stderr
        if not report_data.strip() and result.returncode != 0:
            return {
                "is_valid": False,
                "status": "error",
                "info": {},
                "errors": [f"Mustang CLI execution failed: {stderr_data.strip()}"],
                "raw_xml": ""
            }
            
        return parse_mustang_xml(report_data)
        
    except Exception as e:
        return {
            "is_valid": False,
            "status": "error",
            "info": {},
            "errors": [f"Subprocess execution failed: {str(e)}"],
            "raw_xml": ""
        }
    finally:
        # Always clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
