# Disclaimer

**UAFT (Universal Automation Framework Tool)** is provided "as is" without warranty of any kind, express or implied.

## Usage Risks

By using this software, you acknowledge and agree that:

1.  **Data Loss**: Commands like `uaft cleanup` are designed to delete files. While safeguards (like confirmation prompts and `--dry-run`) are in place, you are solely responsible for ensuring that important data is not lost. Always verify configurations in `uaft.json`.
2.  **Code Modification**: Commands like `uaft fix` modify your source code automatically. It is recommended to use version control (git) to review changes before committing them.
3.  **Execution of Commands**: UAFT executes shell commands defined in `uaft.json`. You are responsible for ensuring that these commands are safe and appropriate for your environment.

## Liability

In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

## No Professional Advice

This tool is intended for development and automation purposes. It does not constitute professional advice or a guarantee of code quality or security.
