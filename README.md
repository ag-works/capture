# Capture Errors

A python package that captures the exceptions and notify them via different methods of notification. 

This package provides the complete context of the runtime errors which help developers debug the issues and saves time in bug fixing.


## Installation

Use the command `pip` to install the package
```bash
$ pip install capture-errors
```


## Environment Setup
```bash
$ export CAPTURE_EMAIL_HOST=smtp.gmail.com
$ export CAPTURE_EMAIL_PORT=465
$ export CAPTURE_EMAIL_USER=username@gmail.com
$ export CAPTURE_EMAIL_PASSWORD=securePassxxxx
```

## Usage

```python
from capture import Capture
from capture.adapters.email import EmailAdapter

capture = Capture()
email_adapter_properties = {
    'from_email': '<email-address>',
    'recipients': '<email-address>',
}
capture.set_adapter(EmailAdapter, email_adapter_properties)

try:
    # Code that can generate an error
    # For example: ZeroDivisionError
    x = 10
    y = 500000
    while True:
        remainder = y % x 
        x -= 1
except Exception as ex:
    capture.push(ex)
```

## Available Adapters

* EmailAdapter

