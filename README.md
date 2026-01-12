## LDAP Injection

LDAP (Lightweight Directory Access Protocol) is a protocol commonly used for authentication and authorization in environments such as Active Directory (AD) and other directory services.

LDAP injection is conceptually similar to SQL injection, but instead of manipulating SQL queries, the attacker manipulates LDAP filter queries used by the application to authenticate users.

## Basic Concept

Applications often build LDAP queries by directly embedding user-supplied input into an LDAP filter.
For example:
```
(&(uid=)(userPassword=))
```

If user input is not properly sanitized, an attacker can alter the structure of the LDAP query itself.

LDAP supports the * wildcard, which matches any value. This can be abused to bypass authentication checks.

### Example:
```
(&(uid=a*)(userPassword=*))
```

uid=a* matches any user whose username starts with a

userPassword=* matches any password

If an administrative account matches this filter, the application may grant admin-level access.

## LDAP Injection via Query Manipulation

Consider an application that builds its LDAP query like this:
```
(&(uid={userInput})(userPassword={passwordInput}))
```

If the username field is injectable, an attacker can supply a payload such as:
```
*)(|(&
```

This transforms the query into:
```
(&(uid=*)(|(&)(userPassword=anyValue))

```
### Explanation:

uid=* matches all users

(|(&)) introduces a logical condition that always evaluates to true

The password check becomes irrelevant

As a result, the entire LDAP filter evaluates as true, bypassing authentication.

## Blind LDAP Injection

In some cases, the application does not return detailed error messages or query results.
This is known as Blind LDAP Injection.

Even without explicit errors, attackers can still infer information by:

- Sending crafted inputs (such as wildcards or injected logic)

- Observing differences in application responses (status codes, redirects, content length, etc.)

For example, testing inputs character by character:
```
a*)(|(&
```

By analyzing how the application responds to each request, it may be possible to enumerate valid usernames or other directory attributes without direct feedback.

## Summary

LDAP injection occurs when user input is unsafely embedded into LDAP filters

Wildcards (*) and logical operators can be abused to bypass authentication

Poor input validation can result in full authentication bypass

Blind LDAP injection relies on response behavior rather than explicit errors
