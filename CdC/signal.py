def populate_models(**kwargs):
    from django.contrib.auth.models import Group, Permission, User
    from django.contrib.contenttypes.models import ContentType
    from .models import Equipment
    User.objects.create_superuser(username="lucas",password="ldos").save()
    groupCanMove, created = Group.objects.get_or_create(name="canMove")
    groupCanReceive, created = Group.objects.get_or_create(name="canReceive")
    groupCanSeeLog, created = Group.objects.get_or_create(name="canSeeLog")
    groupCanManage, created = Group.objects.get_or_create(name="canManagerUser")
    content_type=ContentType.objects.get_for_model(Equipment)
    permissionsCanMove = Permission.objects.create(codename="can_move", name="Can Move Equipments", content_type=content_type)
    permissionsCanReceive = Permission.objects.create(codename="can_receive", name="Can Receive Equipments", content_type=content_type)
    permissionsCanSeeLog = Permission.objects.create(codename="can_see_log", name="Can See logs", content_type=content_type)
    permissionsCanManager = Permission.objects.create(codename="can_manager_user", name="Can Manager Users", content_type=content_type)
    groupCanMove.permissions.add(permissionsCanMove)
    groupCanReceive.permissions.add(permissionsCanMove,permissionsCanReceive)
    groupCanSeeLog.permissions.add(permissionsCanMove,permissionsCanReceive,permissionsCanSeeLog)
    groupCanManage.permissions.add(permissionsCanMove,permissionsCanReceive,permissionsCanSeeLog,permissionsCanManager)