
# External Captive Portal (ExtCP) for Alcatel-Lucent OmniAccess Stellar WLAN

**ExtCP** is a basic implementation of captive portal for Alcatel-Lucent OmniSwitch Stellar WLAN.  The code is writing in python.

---

## 🛠️ Built With

- **python 3.8**

```python
    dependencies = [
        fastapi==0.110.0
        uvicorn[standard]==0.29.0
        python-dotenv==1.0.1
        pydantic-settings==2.2.1
        Jinja2==3.1.4
    ]
```

## 🚀 Installation


1. Clone the git repository and extract the folder into your machine

2. Create a venv environment for python

```python

    python -m venv venv

```
3. Active the virtual environment

```python

    source venv\bin\activate   

    or

    venv\Script\activate

```

4. Install the dependencies 

```python

    pip install -r requirements.txt

```

5. Start the application

```python

    uvicorn main:app --reload

```

6. Verify the page is loading

```Chrome Browser

    http://server_ip:8000/login/ale?clientmac=000000000000&clientip=1.1.1.1&switchmac=000000000001&switchip=10.1.1.1&ssid=skynet&url=www.google.com

```

## 📦 How it works

When the user joined the wireless network, it will be automatically redirected to the external captive portal
login page.  The administrator has to configure the redirect URL in the stellar access point.

On the Access Point, the redirect URL is configured with:
*	Server IP or FQDN
Ex: 192.168.28.1
*	HTTP or HTTPS mode
*	Redirect URL
This is actually the URI and must have the vendor profile/type reference to match the vendor profile in the external captive portal solution.
Ex: /login/ale


The following parameters are automatically added by the AP in the redirection URL.

| Parameter          | value                                    | Format                                |
|--------------------|------------------------------------------|---------------------------------------|
| clientmac          | Client MAC address                       | (i.e xx:xx:xx:xx:xx:xx)               |
| clientip           | Client IP address                        | (i.e 192.168.1.1)                     |
| switchmac          | AP MAC address                           | (i.e xx:xx:xx:xx:xx:xx)               |
| swicthip           | AP IP address                            | (i.e 192.168.1.1)                     |
| ssid               | ESSID name                               | (i.e xx:xx:xx:xx:xx:xx)               |
| url                | Initial URL triggering the redirection   | (i.e www.google.com)                  |
| errmsg             | Fixed value (i.e. Failure)               | (i.e "authentication failure")        |


Login POST Processing
The external captive portal page provides a Login POST to the client browser.

Login POST Target / Post Action
The Login POST is always targeted to the Access Point.
The form action must be: http(s)://cportal.al-enterprise.com/login
The HTTP or HTTPS mode should solely be determined by the external captive portal server, based on its internal needs to secure the form submission to the AP.
As a workaround, the AP could support a new URL parameter that explicitly specifies the Login URL. 
For example: &loginurl=https://cportal.al-enterprise.com/login
Note:
The actual FQDN for the Login URL and the support of the loginurl parameter still need to be confirmed. 

From attributes
With “ale” vendor type, the form must contain the following attributes
Parameter	Value	                                            Comment
user	    The username	
password	The password	
url	        The “landing” URL when authentication passed	
onerror	    The “landing” URL when the authentication failed	Optional 

POST Response
The Access Point always responds with HTTP 200 OK, irrespective of the RADIUS request results.
The HTTP 200 OK simply specifies a new URL to load on the browser.

The URL is constructed as follow:
*	Radius authentication passed
The URL is the “url” specified in the form 
*	Radius authentication failed
    +	If the form has the “onerror” attribute, the URL is the value of this attribute
    +	If the form does not have the “onerror” attribute, the URL is the original redirection URL with all the URL parameters and appended with the “errmsg=Failure” parameter.


If the external captive portal is also the radius server.

RADIUS Attributes
In Access-Request the following attributes must be supported for the “ale” vendor type.

![Imgur Image](https://github.com/Samuelyip74/StellarExternalCP/blob/main/images/radius_attributes.JPG)

Other standard attributes are also included, but they should not be used for any decision making in the external Radius server.
For example: NAS-IP-Address, NAS-Identifier, NAS-Port-Type

Same, Alcatel VSA attributes are included, but they should not be used for any decision making in the external Radius server. For display purposes, we can provide the dictionary.alcatel file.

 * The external captive portal solution must support the Called-Station-ID “apmac:SSID” 

 * The external captive portal solution should not impose a fixed MAC address format  

Access-Accept RADIUS Attributes

In MAC and Portal Authentication, the Access Point supports the following attributes:
![Imgur Image](https://github.com/Samuelyip74/StellarExternalCP/blob/main/images/radius_accept_attributes.JPG)

RADIUS Accounting

No additional requirement for RADIUS accounting.
Similar to Access-Request, the following attributes must be supported for the “ale” vendor type.
![Imgur Image](https://github.com/Samuelyip74/StellarExternalCP/blob/main/images/radius_accounting.JPG)

Accounting attributes
The Access point supports the standard attributes in the Start, Interim and Stop Request
*	User-Name:		This is user-name provided in the Access-Accept
*	Acct-Session-ID:		This is unique per session
*	Acct-Input-Octets
*	Acct-Input-Gigawords
*	Acct-Input-Packets
*	Acct-Output-Octets
*	Acct-Output-Gigawords
*	Acct-Output-Packets
*	Acct-Session-Time
*	Acct-Terminate-Cause (only in Stop)

Other standard attributes or Alcatel VSA are also included, but they should not be used for any decision making in the external Radius server. For example: NAS-IP-Address, NAS-Identifier, NAS-Port-Type

 * The external captive portal solution must support the Called-Station-ID “apmac:SSID” 

 * The external captive portal solution should not impose a fixed MAC address format  



## 📦 Releases

| Version          | Date       | Notes                       |
|------------------|------------|-----------------------------|
| v1.0.1           | 2025-08-15 | First release               |


---

## 📄 License

```
Copyright (c) Samuel Yip Kah Yean <2025>

This software is licensed for personal, non-commercial use only.

You are NOT permitted to:
- Use this software for any commercial purposes.
- Modify, adapt, reverse-engineer, or create derivative works.
- Distribute, sublicense, or share this software.

All rights are reserved by the author.

For commercial licensing or permission inquiries, please contact:
kahyean.yip@gmail.com
```


