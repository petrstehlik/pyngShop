import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';

@Injectable()
export class OrderService {

	constructor(private http : Http) {}

	fetchAll() {
        return this.http.get('/orders')
            .map((r : Response) => {
                return r.json();
            })
            .catch(this.handleError);
    }

    fetch(id : Number) {
        return this.http.get('/orders/' + Number(id))
            .map((r : Response) => {
                return r.json();
            })
            .catch(this.handleError);
    }

    add(item : Object) {
        return this.http.post('/orders', JSON.stringify(item))
            .map((r : Response) => {
                return r.json();
            })
            .catch(this.handleError);
    }

    update(item : Object) {
        return this.http.put('/orders/' + Number(item["id"]), JSON.stringify(item))
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
