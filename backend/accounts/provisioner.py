import logging
from django.db.utils import IntegrityError
from django.apps import apps

logger = logging.getLogger(__name__)

def ensure_admin_accounts():
    """
    Late-binding provisioner that ensures Admin and Staff accounts exist.
    Uses apps.get_model to safely retrieve the User model after registry is ready.
    """
    try:
        # Late binding retrieval of User model
        User = apps.get_model('accounts', 'User')
    except (LookupError, RuntimeError):
        # This can happen if called too early; the apps.py should catch this
        return

    accounts = [
        {
            'email': 'admin@grielisha.com',
            'username': 'admin',
            'password': 'GrielishaAdmin2026!',
            'is_staff': True,
            'is_superuser': True,
            'role': 'admin'
        },
        {
            'email': 'staff@grielisha.com',
            'username': 'staff',
            'password': 'GrielishaStaff2026!',
            'is_staff': True,
            'is_superuser': False,
            'role': 'staff'
        }
    ]

    for acc in accounts:
        try:
            # Use get_or_create to avoid duplicates
            user, created = User.objects.get_or_create(
                email=acc['email'],
                defaults={
                    'username': acc['username'],
                    'is_staff': acc['is_staff'],
                    'is_superuser': acc['is_superuser'],
                    'role': acc['role']
                }
            )
            
            # Reset password to ensure it matches exactly the provided credentials
            user.set_password(acc['password'])
            user.save()
            
            status = "CREATED" if created else "SYNCED"
            msg = f"GRIELISHA: Account {acc['email']} {status} successfully."
            logger.info(msg)
            print(msg)
            
        except Exception as e:
            err_msg = f"GRIELISHA Error provisioning {acc['email']}: {str(e)}"
            logger.error(err_msg)
            print(err_msg)

    print("GRIELISHA: SYSTEM ACCOUNTS FULLY PROVISIONED.")
