import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { CategoryService } from 'app/services/category.service';

@Component({
  selector: 'app-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.scss'],
  providers : [CategoryService]
})
export class CategoryComponent implements OnInit {

    id = null;
    category : Array<Object> = [];

    constructor(private route: ActivatedRoute,
               private categoryService : CategoryService) {}

    ngOnInit() {
        this.route.params.subscribe(params => {
            this.id = +params['id']; // (+) converts string 'id' to a number

            this.getProducts();

            // In a real app: dispatch action to load the details here.
        });
    }

    getProducts() {
        this.categoryService.fetch(this.id).subscribe(
            data => {
                this.category = data;
            },
            error => {
                console.log(error);
            }
        );
    }

}
