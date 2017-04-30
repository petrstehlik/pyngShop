//import { dummyModule } from 'modules/dummy/dummy.module';
import { usersModule } from './modules/users/users.module';

import { CategoryModule } from './modules/category/category.module';
import { ProductModule } from './modules/product/product.module';

export const modules : Array<Object> = [
	CategoryModule,
	ProductModule,
	usersModule
]
