import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';


@Injectable()
export class CategoryService {

    constructor(private http : Http) {
    }

    fetchAll() {
        return this.http.get('/categories')
            .map((r : Response) => {
                let response = r.json();

                return response;
            })
            .catch(this.handleError);
    }

    fetch(id : Number) {
        return this.http.get('/categories/' + Number(id))
            .map((r : Response) => {
                let response = r.json();

                return response;
            })
            .catch(this.handleError);
    }

    delete(id : Number) {
        return this.http.delete('/categories/' + Number(id))
            .map((r : Response) => {
                let response = r.json();

                return response;
            })
            .catch(this.handleError);
    }

    add(item : Object) {
    	item["hidden"] = false;
        return this.http.post('/categories', JSON.stringify(item))
            .map((r : Response) => {
                let response = r.json();

                return response;
            })
            .catch(this.handleError);
    }

    update(item : Object) {
        return this.http.put('/categories/' + Number(item["id"]), JSON.stringify(item))
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
