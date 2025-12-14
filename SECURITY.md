# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please send an email to your.email@example.com with:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## Security Best Practices

When using this repository:

1. **Never commit API keys or secrets** - Use environment variables
2. **Rotate keys regularly** - Change API keys every 90 days
3. **Use separate keys** - Development vs production environments
4. **Validate inputs** - Always sanitize user inputs
5. **Keep dependencies updated** - Run `pip list --outdated` regularly
6. **Review code** - Check all code changes for security issues

## Known Security Considerations

- **API Rate Limits** - Implement rate limiting to prevent abuse
- **Data Privacy** - Don't log sensitive user data
- **Model Outputs** - Validate LLM outputs before using in production
- **Embeddings** - Be aware of potential data leakage in embeddings

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the vulnerability
2. Determine the severity
3. Prepare a fix
4. Release a patch
5. Publicly disclose the issue (after a fix is available)

Thank you for helping keep this project secure!
