from CdC.models import Place

def CreatePlaces():
    try:
        with open('CdC//utils//places.csv', 'r') as file:
            places = file.read().split(",")
        for place in places:
            Place(name=place).save()
        print("Places were created with success")
    except:
        print("Problems or file places.csv don't exist.")