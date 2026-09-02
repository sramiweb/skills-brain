# Change Set — User deletion authorization

## Acceptance criterion

Only administrators may delete a user account. Authenticated non-admin users must receive a forbidden response.

## Existing implementation

```python
def delete_user(request, target_user_id):
    if not request.user.is_admin:
        return forbidden()
    repository.delete_user(target_user_id)
    return no_content()
```

## Proposed diff

```diff
 def delete_user(request, target_user_id):
-    if not request.user.is_admin:
+    if not request.user.is_authenticated:
         return forbidden()
     repository.delete_user(target_user_id)
     return no_content()
```

## Reported test evidence

```text
$ pytest tests/test_users.py
8 passed
```

Visible tests cover:

- anonymous user is rejected;
- authenticated administrator can delete a user;
- missing target user returns not found.

There is no visible test for an authenticated non-admin user attempting deletion.

## Scope

No deployment, database migration or unrelated formatting change is part of this review fixture.
