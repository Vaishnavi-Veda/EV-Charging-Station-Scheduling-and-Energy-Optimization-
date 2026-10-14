from vehicles import Vehicle, Bike, Car, SUV, Truck

class ParkingSpot:
    sizes = ['S', 'M', 'L', 'XL']
    def __init__(self, size=sizes[0]):
        self.size = size
        self.vehicle = None
    
    def assign_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle
        vehicle.parking_spot = self
    
    def remove_vechicle(self, hours=1):
        cost = self.vehicle.calc_parking_fee(hours)
        vehicle = self.vehicle = None
        self.vehicle.parking_spot = None
        return vehicle, cost
    
    def display(self):
        print(f'Size: {self.size}')
        print(f'Slot Status: ')
        if self.vehicle:
            self.vehicle.display()


class ParkingLot:
    SIZES = {
        'S': 1,
        'M': 2,
        'L': 3,
        'XL': 4
    }
    
    def __init__(self, lot_name: str = 'Parking Lot'):
        self.spots = {
            'S': [],
            'M': [],
            'L': [],
            'XL': []
        }
        self.lot_name = lot_name
    
    def add_spot(self, spot: ParkingSpot):
        size = spot.size
        match size:
            case 'S': self.spots['S'].append(spot)
            case 'M': self.spots['M'].append(spot)
            case 'L': self.spots['L'].append(spot)
            case 'XL': self.spots['XL'].append(spot)
    
    def show_spots(self):
        for size in self.spots:
            print('-'*30)
            print(f'Size: {size}')
            print('-'*30)
            for spot in self.spots[size]:
                spot.display()
        print('-'*30)
    
    def park_vehicle(self, vehicle: Vehicle):
        '''
            Returns True if spot is assigned, else returns False
        '''
        if isinstance(vehicle, Bike):
            min_size = 'S'
        elif isinstance(vehicle, Car):
            min_size = 'M'
        elif isinstance(vehicle, SUV):
            min_size = 'L'
        elif isinstance(vehicle, Truck):
            min_size = 'XL'
        else:
            min_size = 'S'
        
        for size in self.spots:
            if self.SIZES[min_size] <= self.SIZES[size]:
                for spot in self.spots[size]:
                    if not spot.vehicle:
                        spot.assign_vehicle(vehicle)
                        return True

        return False
    
    def unpark_vehicle(self, plate: str, hours: int=1):
        '''
            Returns cost calculated based on hours
        '''
        # Search for vehicle and delete based on vehicle plate
        for size in self.spots:
            for spot in self.spots[size]:
                if spot.vehicle and spot.vehicle.plate == plate:
                    vehicle = spot.vehicle
                    spot.vehicle = None
        
        cost = hours * vehicle.fee_per_hour
        
        return cost, vehicle
    

