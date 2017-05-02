import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';

@Injectable()
export class ProductService {

  constructor(private http : Http) {}

  fetchAll() {
        return this.http.get('/products')
            .map((r : Response) => {
                let response = r.json();

                return response;
            })
            .catch(this.handleError);
    }

    fetch(id : Number) {
        return this.http.get('/products/' + Number(id))
            .map((r : Response) => {
                let response = r.json();

                return response;
            })
            .catch(this.handleError);
    }

    delete(id : Number) {
        return this.http.delete('/products/' + Number(id))
            .map((r : Response) => {
                let response = r.json();

                return response;
            })
            .catch(this.handleError);
    }

    add(item : Object) {
    	item["hidden"] = false;
        return this.http.post('/products', JSON.stringify(item))
            .map((r : Response) => {
                let response = r.json();

                return response;
            })
            .catch(this.handleError);
    }

    update(item : Object) {
        return this.http.put('/products/' + Number(item["id"]), JSON.stringify(item))
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
