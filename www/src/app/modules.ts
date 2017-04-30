//import { dummyModule } from 'modules/dummy/dummy.module';
import { usersModule } from './modules/users/users.module';

<<<<<<< HEAD
export const modules : Array<Object> = [
=======
import { CategoryModule } from './modules/category/category.module';
import { ProductModule } from './modules/product/product.module';

export const modules : Array<Object> = [
	CategoryModule,
	ProductModule,
>>>>>>> e0bddf3... Add base for modules
	usersModule
]
