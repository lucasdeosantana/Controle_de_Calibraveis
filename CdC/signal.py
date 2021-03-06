def populate_models(**kwargs):
    from django.contrib.auth.models import Group, Permission, User
    from django.contrib.contenttypes.models import ContentType
    from .models import Equipment, Place
    try:
        adminUser = User.objects.create_user(username="admin",password="admin")
        adminUser.save()
        print("Admin User was created.")
    except:
        pass
    try:
        Place(name="Base").save()
        print("Base place was created")
    except:
        pass
    groupCanMove, created = Group.objects.get_or_create(name="Can Move")
    groupCanReceive, created = Group.objects.get_or_create(name="Can Receive")
    groupCanSeeLog, created = Group.objects.get_or_create(name="Can See Log")
    groupCanManagerUser, created = Group.objects.get_or_create(name="CanManagerUser")
    groupCanManagerEquipment, created = Group.objects.get_or_create(name="Can Manager Equipment")
    print("Groups were created!")
    content_type=ContentType.objects.get_for_model(Equipment)
    permissionsCanMove = Permission.objects.create(codename="can_move", name="Can Move Equipments", content_type=content_type)
    permissionsCanReceive = Permission.objects.create(codename="can_receive", name="Can Receive Equipments", content_type=content_type)
    permissionsCanSeeLog = Permission.objects.create(codename="can_see_log", name="Can See logs", content_type=content_type)
    permissionsCanManagerUser = Permission.objects.create(codename="can_manager_user", name="Can Manager Users", content_type=content_type)
    permissionsCanManagerEquipment = Permission.objects.create(codename="can_manager_equipment", name="Can Manager Equipments", content_type=content_type)
    print("Permissions were created")
    groupCanMove.permissions.add(permissionsCanMove)
    groupCanReceive.permissions.add(permissionsCanMove,permissionsCanReceive)
    groupCanSeeLog.permissions.add(permissionsCanMove,permissionsCanReceive,permissionsCanSeeLog)
    groupCanManagerEquipment.permissions.add(permissionsCanMove,permissionsCanReceive,permissionsCanSeeLog,permissionsCanManagerEquipment)
    groupCanManagerUser.permissions.add(permissionsCanMove,permissionsCanReceive,permissionsCanSeeLog,permissionsCanManagerEquipment,permissionsCanManagerUser)
    print("Groups were created")
    adminUser.groups.add(groupCanManagerUser)
    print("Admin User is Group Can Manager User")
    from .utils.createPlaces import CreatePlaces
    CreatePlaces()