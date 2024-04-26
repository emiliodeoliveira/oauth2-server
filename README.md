# Overview
This repository contains the Guardian Gate, an OAuth2 server developed in Python. It provides endpoints for user authentication, authorization, and secure access to API resources.

## Features
- Authentication Flow: Implement the OAuth2 authorization code flow.
- Token Exchange: Exchange authorization codes for access tokens.
- Access Control: Verify access tokens for protected resources.
- Token Expiry and Refresh: Handle token expiration and refresh.
- Error Handling: Return appropriate error responses.

### Getting Started
Clone this repository:

```bash
 git clone https://github.com/emiliodeoliveira/oauth2-server.git 
 ```

Install dependencies:

```bash
 $ pip install -r requirements.txt 
 ```

Set the environment variables:

```bash
 $ export FLASK_APP=app.py 
```
If you want to enable the debug mode, please set this:

```bash
$ export FLASK_DEBUG=1
```

If you want to disable the HTTPS for development purposes, please set this. But please, dont use this in production!
```bash
$ export AUTHLIB_INSECURE_TRANSPORT=1
```
### Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.