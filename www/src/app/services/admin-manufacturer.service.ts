import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

@Injectable()
export class AdminManufacturerService {

	constructor(private http : Http) { }

	add(manufacturer : Object) {
		return this.http.post('/manufacturers', JSON.stringify(manufacturer))
		.map((response : Response) => {
			return response.json();
		}).catch(this.handleError);
	}

	remove(id : string) {
		return this.http.delete('/manufacturers/' + id)
		.map((response : Response) => {
			return response.json();
		}).catch(this.handleError);
	}

	fetchAll() {
		return this.http.get('/manufacturers')
		.map((response : Response) => {
			return response.json();
		}).catch(this.handleError);
	}

	fetch(id : String) {
		return this.http.get('/manufacturers/' + id)
			.map((response: Response) => {
				return response.json();
			})
			.catch(this.handleError);
	}

	update(id : String, user : Object) {
		return this.http.put('/manufacturers/' + id, user)
			.map((response: Response) => {
				let manufacturer : Object = response.json();
				return manufacturer;
			})
			.catch(this.handleError);
	}

	private handleError(err : Response | any) {
		console.log(err);
		return Promise.reject(err);
	}

}
