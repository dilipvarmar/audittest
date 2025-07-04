# asa_audit.py

import re
from pathlib import Path

# === Config ===
CONFIG_FILE = "sample_config.txt"

# === Sample Rules ===
RULES = [
    {
        "name": "Permit Any-Any ACL",
        "pattern": r"access-list .* permit ip any4 any4",
        "severity": "High",
        "message": "Unrestricted IP access found. Replace 'any4 any4' with specific subnets."
    },
    {
        "name": "Weak SSH DH Group",
        "pattern": r"ssh key-exchange group dh-group1-sha1",
        "severity": "High",
        "message": "Weak SSH key exchange group (dh-group1-sha1). Use dh-group14-sha256 or higher."
    },
    {
        "name": "External SSH Access",
        "pattern": r"ssh \d+\.\d+\.\d+\.\d+ \d+\.\d+\.\d+\.\d+ outside",
        "severity": "Medium",
        "message": "SSH access from external IP. Ensure only trusted IPs are allowed."
    },
    {
        "name": "Multiple Privileged Users",
        "pattern": r"username .* privilege 15",
        "severity": "Medium",
        "message": "Multiple users with privilege 15. Consider RBAC and central authentication."
    },
    {
        "name": "IKEv1 VPN Detected",
        "pattern": r"crypto ikev1 enable",
        "severity": "Medium",
        "message": "IKEv1 VPN is enabled. Consider migrating to IKEv2 with certificate-based auth."
    }
]

# === Functions ===
def load_config(path):
    return Path(path).read_text()

def audit_config(config_text):
    findings = []
    for rule in RULES:
        matches = re.findall(rule["pattern"], config_text)
        if matches:
            findings.append({
                "rule": rule["name"],
                "severity": rule["severity"],
                "message": rule["message"],
                "matches": matches
            })
    return findings

def print_report(findings):
    if not findings:
        print("✅ No critical issues found.")
        return
    print("\n🔍 Security Audit Report:\n")
    for finding in findings:
        print(f"🚨 {finding['rule']} ({finding['severity']})")
        print(f"    {finding['message']}")
        for m in finding['matches']:
            print(f"    ↳ {m}")
        print()

# === Main ===
if __name__ == "__main__":
    print("🔧 Running ASA Config Audit Tool...")
    config = load_config(CONFIG_FILE)
    results = audit_config(config)
    print_report(results)
