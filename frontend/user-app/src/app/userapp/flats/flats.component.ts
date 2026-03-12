import { Component, OnInit } from '@angular/core';
import { FlatService } from '../services/flat.service';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-flats',
  templateUrl: './flats.component.html',
  standalone: true,
  imports: [CommonModule, RouterModule, HttpClientModule, FormsModule]
})
export class FlatsComponent implements OnInit {

  flats: any[] = [];
  allFlats: any[] = [];

  loading: boolean = true;
  errorMsg: string = '';

  towers: string[] = [];
  locations: string[] = [];
  flatNumbers: string[] = [];
  flatTypes: string[] = [];
  flatFloors: string[] = [];

  amenitiesList: string[] = [];
  selectedAmenity: string = '';


  selectedTower: string = '';
  selectedLocation: string = '';
  selectedPriceRange: string = '';

  selectedFlatNumber: string = '';
  selectedFlatType: string = '';

  isLoggedIn = false;

  showAvailableOnly: boolean = false;
  selectedFlatFloor: string = '';
  
  priceRanges: string[] = [
    '0-5000',
    '5000-10000',
    '10000-20000',
    '20000+'
  ];

  constructor(
    private flatService: FlatService,
    private router: Router
  ) {}

  // ⭐ Load Flats

ngOnInit(): void {
  const token = localStorage.getItem('access_token');
  this.isLoggedIn = !!token;

  this.loadFlats(); // load flats
}
  // ⭐ Load Flats From API
  loadFlats() {
  this.loading = true; // Set loading to true at start
  this.flatService.getAllFlats().subscribe({
    next: (data: any) => {
      console.log("DEBUG: Data received from API:", data);
      // Since your Flask return is a direct array [...], 'data' is already the array
      if (!Array.isArray(data)) {
        console.error("Data is not an array:", data);
        this.errorMsg = "Invalid data format received";
        this.loading = false;
        return;
      }

      this.flats = data;
      this.allFlats = [...data]; // Create a copy for filtering
      
      // Populate your filter dropdowns dynamically from the DB data
this.towers = [...new Set(data.map((f: any) => f.tower_name))].filter(Boolean);
this.locations = [...new Set(data.map((f: any) => f.location))].filter(Boolean);
this.flatTypes = [...new Set(data.map((f: any) => f.flat_type))].filter(Boolean);
      
      this.loading = false; // Data is here, stop the spinner
    },
    error: (err) => {
      console.error(err);
      this.errorMsg = "Failed to load flats from Database";
      this.loading = false;
    }
  });
}
  getAmenitiesText(amenities: any): string {
  if (!amenities) return 'Not specified';

  // 1. If it's already a proper Array
  if (Array.isArray(amenities)) {
    return amenities.join(', ');
  }

  // 2. If it's a string that looks like "["Pool", "Gym"]"
  if (typeof amenities === 'string') {
    try {
      // Try to parse it into an array
      const parsed = JSON.parse(amenities);
      if (Array.isArray(parsed)) {
        return parsed.join(', ');
      }
    } catch (e) {
      // If it's just a normal string like "Pool, Gym", return it
      return amenities;
    }
  }

  return 'Not specified';
}

  


bookNow(flatId: number) {

  const confirmBooking = confirm("Do you want to book this flat?");

  if (!confirmBooking) {
    return; // user clicked Cancel
  }

  const token = localStorage.getItem('access_token');

  if (!token) {
    alert("Please login to book flat");

    this.router.navigate(['/auth'], {
      queryParams: { returnUrl: `/booking-confirm/${flatId}` }
    });

    return;
  }

  // If logged in → go normally
  this.router.navigate(['/booking-confirm', flatId]);
}

// filterFlats() {

//   this.flats = this.allFlats.filter(flat => {

//     return (
//       (!this.selectedTower || flat.tower_name === this.selectedTower) &&
//       (!this.selectedLocation || flat.location === this.selectedLocation) &&
//       (!this.selectedFlatNumber || flat.flat_number == this.selectedFlatNumber) &&
//       (!this.selectedFlatType || flat.flat_type === this.selectedFlatType)
//     );

//   });

// }

  // ⭐ Filter Flats
  filterFlats() {

    this.flats = this.allFlats.filter(flat => {

      const towerMatch = this.selectedTower
        ? flat.tower_name === this.selectedTower
        : true;

      const locationMatch = this.selectedLocation
        ? flat.location === this.selectedLocation
        : true;

        const flatTypeMatch = this.selectedFlatType
        ? flat.flat_type === this.selectedFlatType
        : true;

        const flatNumberMatch = this.selectedFlatNumber
        ? flat.flat_number === this.selectedFlatNumber
        : true;

 const flatFloorMatch = this.selectedFlatFloor
  ? flat.floor == this.selectedFlatFloor
  : true;

  const amenityMatch = this.selectedAmenity
  ? flat.amenities?.includes(this.selectedAmenity)
  : true;

      let priceMatch = true;

      if (this.selectedPriceRange) {

        const price = flat.price;

        if (this.selectedPriceRange === '0-5000')
          priceMatch = price >= 0 && price <= 5000;

        else if (this.selectedPriceRange === '5000-10000')
          priceMatch = price > 5000 && price <= 10000;

        else if (this.selectedPriceRange === '10000-20000')
          priceMatch = price > 10000 && price <= 20000;

        else if (this.selectedPriceRange === '20000+')
          priceMatch = price > 20000;
      }
      
          const availabilityMatch = this.showAvailableOnly
      ? !flat.is_booked   // Change to flat.status !== 'booked' if using status column
      : true;

      return towerMatch && locationMatch && priceMatch && flatTypeMatch && flatNumberMatch && availabilityMatch && flatFloorMatch && amenityMatch;

    });
    

  }
  resetFilters() {
  this.selectedLocation = "";
  this.selectedFlatType = "";
  this.selectedTower = "";
  this.selectedPriceRange = "";
  this.selectedFlatNumber = "";

  this.flats = this.allFlats;
}
sortOption: string = "";

sortFlats() {
  if (this.sortOption === "low") {
    this.flats.sort((a, b) => a.price - b.price);
  } else if (this.sortOption === "high") {
    this.flats.sort((a, b) => b.price - a.price);
  }
}

}