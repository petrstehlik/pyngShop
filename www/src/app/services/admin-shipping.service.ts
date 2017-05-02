import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

@Injectable()
export class AdminShippingService {


	constructor(private http : Http) { }

	add(shipping : Object) {
		return this.http.post('/shippings', JSON.stringify(shipping))
		.map((response : Response) => {
			return response.json();
		}).catch(this.handleError);
	}

	remove(id : string) {
		return this.http.delete('/shippings/' + id)
		.map((response : Response) => {
			return response.json();
		}).catch(this.handleError);
	}

	fetchAll() {
		return this.http.get('/shippings')
		.map((response : Response) => {
			return response.json();
		}).catch(this.handleError);
	}

	fetch(id : String) {
		return this.http.get('/shippings/' + id)
			.map((response: Response) => {
				return response.json();
			})
			.catch(this.handleError);
	}

	update(id : String, ship : Object) {
		return this.http.put('/shippings/' + id, ship)
			.map((response: Response) => {
				let shipping : Object = response.json();
				return shipping;
			})
			.catch(this.handleError);
	}

	private handleError(err : Response | any) {
		console.log(err);
		return Promise.reject(err);
	}

}
