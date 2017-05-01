import { Component, OnInit } from '@angular/core';

import {CategoryService } from 'app/services/category.service';

@Component({
  selector: 'category-bar',
  templateUrl: './category-bar.component.html',
  styleUrls: ['./category-bar.component.scss'],
  providers : [CategoryService]
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

    constructor(private category : CategoryService) { }

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

}
