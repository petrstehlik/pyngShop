import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';

@Injectable()
export class StatsService {

	constructor(private http : Http) {}

	orders() {
		return this.http.get('/stats/orders?products_count=10')
            .map((r : Response) => {
                let response = r.json();

                return response;
            })
            .catch(this.handleError);
	}

	products() {
		return this.http.get('/stats/products?products_count=10')
            .map((r : Response) => {
                let response = r.json();

                return response;
            })
            .catch(this.handleError);
	}

	private handleError(err : Response | any) {
        console.log(err);
        return Promise.reject(err);
    }

}
