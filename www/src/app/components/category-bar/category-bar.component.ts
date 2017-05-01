import { Component, OnInit } from '@angular/core';

<<<<<<< HEAD
import {CategoryService } from 'app/services/category.service';
import {UserService } from 'app/services/user.service';

@Component({
  selector: 'category-bar',
  templateUrl: './category-bar.component.html',
  styleUrls: ['./category-bar.component.scss'],
  providers : [CategoryService, UserService]
})
export class CategoryBarComponent implements OnInit {

    categories : Array<Object>;
    newcat = "+ Add Category";
    newsub = "+ Add Subcategory";

    constructor(private category : CategoryService,
               private user : UserService) { }

    ngOnInit() {
    	this.load();
    }

    load() {
		this.category.fetchAll().subscribe(
            data => {
                this.categories = data
            },
            error => {
                console.log(error);
            }
        );
    }

    saveEditable(event : any) {
        if (event == "+ Add Category") {
            return;
        }

        this.category.add({"name" : event}).subscribe(
			data => {
				this.load();
				this.newcat = "+ Add Category";
			},
			error => {
				console.log(error);
				this.newcat = "+ Add Category";
			}
    	);

    }

    newSubCat(event, id : Number) {
    	if (event == "+ Add Subcategory") {
			return;
    	}

    	this.category.add({"name" : event, "parent" : {"id" : id}, "hidden" : false}).subscribe(
			data => {
				this.load();
				this.newsub = "+ Add Subcategory";
			},
			error => {
				console.log(error);
				this.newsub = "+ Add Subcategory";
			}
    	);
    }
=======
@Component({
  selector: 'category-bar',
  templateUrl: './category-bar.component.html',
  styleUrls: ['./category-bar.component.scss']
})
export class CategoryBarComponent implements OnInit {

    user = {
        admin : false
    }
    categories = [
        {
            "slug" : "ebooks",
            "name" : "Ebooks",
            "sub" : [
                {
                    "slug" : "beletry",
                    "name" : "Beletry"
                }
            ]

        }
    ]

  constructor() { }

  ngOnInit() {
  }

>>>>>>> 9107357... Components: Category Bar and Item
}
