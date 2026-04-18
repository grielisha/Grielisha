import logging
from django.db.utils import IntegrityError

logger = logging.getLogger(__name__)

def ensure_admin_accounts():
    """
    Fail-safe provisioner that ensures Admin and Staff accounts exist.
    Runs on every server startup via AppConfig.ready().
    """
    from accounts.models import User
    
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
            user, created = User.objects.get_or_create(
                email=acc['email'],
                defaults={
                    'username': acc['username'],
                    'is_staff': acc['is_staff'],
                    'is_superuser': acc['is_superuser'],
                    'role': acc['role']
                }
            )
            
            # Always ensure the password is correct for these specific accounts
            user.set_password(acc['password'])
            user.save()
            
            status = "CREATED" if created else "VERIFIED/UPDATED"
            logger.info(f"GRIELISHA Provisioning: Account {acc['email']} {status}")
            print(f"GRIELISHA Provisioning: Account {acc['email']} {status}")
            
        except Exception as e:
            logger.error(f"GRIELISHA Provisioning Error for {acc['email']}: {str(e)}")
            print(f"GRIELISHA Provisioning Error for {acc['email']}: {str(e)}")

    print("GRIELISHA: All administrative accounts are ready.")
