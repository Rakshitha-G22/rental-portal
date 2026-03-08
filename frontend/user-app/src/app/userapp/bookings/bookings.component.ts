import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { BookingService } from '../services/booking.service';
import { environment } from 'environments/environment';

@Component({
  selector: 'app-bookings',
  standalone: true,
  imports: [CommonModule, HttpClientModule, RouterModule],
  templateUrl: './bookings.component.html',
})
export class BookingsComponent implements OnInit {

  flatId!: number;
  flat: any;
  message = '';
  error = '';
  loading = true;

  isBooked: boolean = false;
  errorMessage: string = '';

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private router: Router,
       private bookingService: BookingService
  ) {}

  ngOnInit() {
    this.flatId = Number(this.route.snapshot.paramMap.get('id'));
    this.fetchFlat();
  }

  fetchFlat() {
    this.http.get<any[]>(`${environment.apiUrl}/flats`)
      .subscribe({
        next: (data) => {
          this.flat = data.find(f => f.id === this.flatId);
          this.loading = false;
        },
        error: () => {
          this.error = 'Error fetching flat.';
          this.loading = false;
        }
      });
  }

  bookFlat(id: number) {
    const token = localStorage.getItem('token');

    this.http.post(
      `${environment.apiUrl}/bookings/book/${id}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    ).subscribe({
      next: () => {
        alert('Booked successfully!');
        this.isBooked = true;
      },
      error: (err) => {
        console.error(err);
        this.errorMessage = 'Booking failed';
      }
    });
  }

  confirmBooking() {
    const token = localStorage.getItem('token');

    if (!token) {
      this.errorMessage = 'You must be logged in to book';
      return;
    }

    this.http.post(
      `${environment.apiUrl}/bookings`,
      { flat_id: this.flat.id },
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    ).subscribe({
      next: (res: any) => {
        alert(res.msg || 'Booking confirmed');
        this.isBooked = true;
      },
      error: (err) => {
        console.error(err);
        this.errorMessage = err.error?.msg || 'Failed to book flat';
      }
    });
  }
}
