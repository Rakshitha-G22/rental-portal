import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Flat {
  id: number;
  flat_number: string;
  flat_type: string;
  location: string;
  tower_name: string;
  floor: number;
  price: number;
  image: string;
  amenities?: string[];
  is_booked?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class FlatService {
  // Ensure your environment.apiUrl is set to 'https://rental-portal-backend-hy1p.onrender.com'
  private baseUrl = environment.apiUrl.replace(/\/$/, ""); 

  constructor(private http: HttpClient) {}

  getAllFlats(): Observable<Flat[]> {
    // This will correctly resolve to: .../flats/
    return this.http.get<Flat[]>(`${this.baseUrl}/flats/`);
  }

  getFlatById(id: number): Observable<Flat> {
    // This will correctly resolve to: .../flats/123
    return this.http.get<Flat>(`${this.baseUrl}/flats/${id}`);
  }
}