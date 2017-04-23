import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
<<<<<<< HEAD
import { HttpModule, Http, Request, XHRBackend, RequestOptions} from '@angular/http';
import { RouterModule, Routes, Router } from '@angular/router';

import {NgbModule} from '@ng-bootstrap/ng-bootstrap';

import { AppComponent } from './app.component';
import { HomeComponent } from './components/';
import { LoginComponent } from './components/';
import { LogoutComponent } from './components/';
import { SetupComponent } from './components/';
import { NullComponent } from './components/';
import { TopBarModule } from './components/topbar/top-bar.module';
import { CustomerLoginComponent } from './components/customer-login/login.component';


import { AuthGuard } from './utils/index';
import { HttpInterceptor } from './utils/index';
import { SafePipe, SafePipeModule } from 'app/utils/safe.pipe';

import { modules } from './modules';
import { CategoryBarComponent } from './components/category-bar/category-bar.component';
import { CategoryItemComponent } from './components/category-item/category-item.component';
import { CategoryComponent } from './components/category/category.component';

import {UserService} from './services/user.service';
import { RegisterComponent } from './components/register/register.component'

import {InlineEditorModule} from 'ng2-inline-editor';
import { ProductCardComponent } from './components/product-card/product-card.component';
import { ProductNewComponent } from './components/product-new/product-new.component';
import { AccountComponent } from './components/account/account.component';
import { CustomFormsModule } from 'ng2-validation';
import { AdminComponent } from './components/admin/admin.component';
import { AdminManufacturerComponent } from './components/admin-manufacturer/admin-manufacturer.component';
import { AdminShippingComponent } from './components/admin-shipping/admin-shipping.component';
//import { Manufacturer } from './components/manufacturer/manufacturer.component';
import { TruncatePipe } from './utils/truncate.pipe';
import { ProductComponent } from './components/product/product.component';
import { CartComponent } from './components/cart/cart.component';
import { TotalPipe } from './utils/total.pipe';
import { AdminOrdersComponent } from './components/admin-orders/admin-orders.component';
import { AdminOrderDetailComponent } from './components/admin-order-detail/admin-order-detail.component';

export const appRoutes: Routes = [
	{
		path : 'admin/login',
		component : LoginComponent
	},
	{
		path : 'admin/manufacturers',
		component : AdminManufacturerComponent
	},
	{
		path : 'admin/shipping',
		component : AdminShippingComponent
	},
	{
		path : 'admin/orders',
		component : AdminOrdersComponent
	},
	{
		path : 'admin/orders/:id',
		component : AdminOrderDetailComponent
	},
	{
		path : 'login',
		component : CustomerLoginComponent
	},
	{
		path : 'logout',
		component : LogoutComponent,
		canActivate : [AuthGuard]
	},
	{
		path : 'register',
		component : RegisterComponent
	},
	{
		path : 'account',
		component : AccountComponent
	},
    {
        path : 'category/:id',
        component : CategoryComponent
    },
	{
		path : 'category/:categoryid/product/new',
		component : ProductNewComponent,
		canActivate : [AuthGuard],
		data : {
			role: 0
		}
	},
	{
		path : 'product/:id',
		component : ProductComponent
	},
	{
		path: 'admin',
		component : AdminComponent,
		canActivate : [AuthGuard],
		data : {
			role : 0
		}
	},
	{
		path : 'cart',
		component : CartComponent
	},
	{
		path: '',
		component: HomeComponent,
		canActivate : []
	},
	{
		path: '**',
		component: NullComponent
	}
];

export function setFactory (xhrBackend: XHRBackend,
				requestOptions: RequestOptions,
				router: Router) {
	return new HttpInterceptor(xhrBackend, requestOptions, router);
}

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    CustomerLoginComponent,
    LogoutComponent,
    SetupComponent,
    NullComponent,
    CategoryBarComponent,
    CategoryItemComponent,
    CategoryComponent,
    ProductCardComponent,
    ProductNewComponent,
    RegisterComponent,
    AccountComponent,
    AdminComponent,
    AdminManufacturerComponent,
    AdminShippingComponent,
   // Manufacturer,
    TruncatePipe,
    ProductComponent,
    CartComponent,
    TotalPipe,
    AdminOrdersComponent,
    AdminOrderDetailComponent
  ],
  imports: [
	modules,
	TopBarModule,
	SafePipeModule,
    BrowserModule,
	FormsModule,
	HttpModule,
	InlineEditorModule,
	CustomFormsModule,
	NgbModule.forRoot(),
	RouterModule.forRoot(appRoutes)
  ],
  providers: [
	AuthGuard,
	UserService,
	SafePipe,
		{
			provide : Http,
			useFactory: setFactory,
			deps: [XHRBackend, RequestOptions, Router]
		}

  ],
=======
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [],
>>>>>>> 10e2375... Angular 4 front-end
  bootstrap: [AppComponent]
})
export class AppModule { }
