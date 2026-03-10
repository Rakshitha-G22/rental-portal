import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private BASE_URL = environment.apiUrl; // picks prod or dev automatically

  constructor(private http: HttpClient) {}

  // ================= AUTH =================
  register(user: { name: string; email: string; password: string }) {
    return this.http.post(`${this.BASE_URL}/auth/register`, user);
  }

  login(credentials: { email: string; password: string }) {
    return this.http.post(`${this.BASE_URL}/auth/login`, credentials);
  }

  // ================= FLATS =================
  getFlats() {
    return this.http.get(`${this.BASE_URL}/flats`);
  }

  // ================= BOOKINGS =================
  confirmBooking(flatId: number, token: string) {
    return this.http.post(
      `${this.BASE_URL}/bookings/book/${flatId}`,
      {},
      this.getAuthHeaders(token)
    );
  }

  requestBooking(flatId: number, token: string) {
    return this.http.post(
      `${this.BASE_URL}/bookings/${flatId}`,
      {},
      this.getAuthHeaders(token)
    );
  }

  getMyBookings(token: string) {
    return this.http.get(
      `${this.BASE_URL}/bookings/my`,
      this.getAuthHeaders(token)
    );
  }

  cancelBooking(bookingId: number, token: string) {
    return this.http.put(
      `${this.BASE_URL}/bookings/cancel/${bookingId}`,
      {},
      this.getAuthHeaders(token)
    );
  }

  downloadReceipt(bookingId: number, token: string) {
    return this.http.get(
      `${this.BASE_URL}/bookings/receipt/${bookingId}`,
      { ...this.getAuthHeaders(token), responseType: 'blob' }
    );
  }

  // ================= HELPERS =================
  private getAuthHeaders(token: string) {
    return { headers: new HttpHeaders({ Authorization: `Bearer ${token}` }) };
  }
}