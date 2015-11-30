# CONFIG = {
# 	'user' : 'pyngshop',
# 	'db' : 'pyngshop',
# 	'passwd' : 'klobaska',
# 	'port' : 9999,
# 	'unix_socket' : '/Applications/MAMP/tmp/mysql/mysql.sock'
# }

CONFIG = {
	'db' : {
		'user' : 'pyngshop',
		'database' : 'pyngshop',
		'password' : 'klobaska',
		'port' : 9999,
	},
	'email' : {
		'username' 	: 'ddujda@seznam.cz',
		'password'	: '******',
		'server'	: 'smtp.seznam.cz',
		'from'		: 'info@pyngshop.bitch'
	},
	#'unix_socket' : '/Applications/MAMP/tmp/mysql/mysql.sock'
	'debug' : True,
	'version' : '/v1'
}