import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Title }     from '@angular/platform-browser';

import { CategoryService } from 'app/services/category.service';
import { UserService } from 'app/services/user.service';

@Component({
  selector: 'app-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.scss'],
  providers : [CategoryService, UserService]
})
export class CategoryComponent implements OnInit {

    id = null;
    category : Array<Object> = [];
    newsubcat = {
		"name" : "Subcategory name"
    }

    message = null;

    constructor(private route: ActivatedRoute,
               private categoryService : CategoryService,
               private user : UserService,
               private title : Title) {}

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
                let title = this.title.getTitle();
				let name = title.split('|');

				this.title.setTitle(name[0] + ' | ' + this.category["name"]);
            },
            error => {
                console.log(error);
            }
        );
    }

    update(event) {
		console.log(this.category)

		this.categoryService.update(this.category).subscribe(
			data => {
				this.category = data;
			},
			err => {
				console.log(err);
			}
		);
    }

	addSubCat(event) {
		if (event == "Subcategory name") {
			return;
		}

		this.categoryService.add({
			"name" : event,
			"parent" : {"id" : this.id},
			"hidden" : false})
		.subscribe(
			data => {
				this.getProducts();
				this.newsubcat["name"] = "+ Add Subcategory";
				this.message = "Subcategory successfully added"
			},
			error => {
				console.log(error);
				this.newsubcat["name"] = "+ Add Subcategory";
				this.message = error["message"];
			}
		);
	}

}
