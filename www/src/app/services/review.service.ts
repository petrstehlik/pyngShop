import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';

@Injectable()
export class ReviewService {

  constructor(private http : Http) {}

    fetch(id : Number) {
        return this.http.get('/products/' + Number(id) + "/reviews")
            .map((r : Response) => {
                return r.json();
            })
            .catch(this.handleError);
    }

    add(id : Number, item : Object) {
        return this.http.post('/products/' + Number(id) + '/reviews', JSON.stringify(item))
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
