from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, personal_id, full_name, email, phone_number, password):
        """ Create a new User. """
        if not personal_id:
            raise ValueError('User must have Personal_id.')
        if not email:
            raise ValueError('User must have Email-Address.')
        if not full_name:
            raise ValueError('User must have Full-Name.')
        if not phone_number:
            raise ValueError('User must have Phone-Number.')

        user = self.model(personal_id=personal_id,
                          full_name=full_name,
                          email=self.normalize_email(email),
                          phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, personal_id, full_name, email, phone_number, password):
        """ Create a new SuperUser. """
        user = self.create_user(personal_id, full_name, email, phone_number, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
