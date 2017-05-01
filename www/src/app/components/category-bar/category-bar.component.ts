import { Component, OnInit } from '@angular/core';

import {CategoryService } from 'app/services/category.service';
import {UserService } from 'app/services/user.service';

@Component({
  selector: 'category-bar',
  templateUrl: './category-bar.component.html',
  styleUrls: ['./category-bar.component.scss'],
  providers : [CategoryService, UserService]
})
export class CategoryBarComponent implements OnInit {

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

    newcat = "+ Add Category";

    constructor(private category : CategoryService,
               private user : UserService) { }

    ngOnInit() {
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
        console.log(event);
    }

}
