create table if not exists xxlw.baidu
(
	id int auto_increment
		primary key,
	area varchar(50) not null,
	parent text not null,
	word varchar(50) not null,
	index_type text not null,
	index_all text not null,
	index_pc text not null,
	index_wise text not null,
	ratio_all text not null,
	ratio_pc text not null,
	ratio_wise text not null,
	range_date int not null,
	constraint w_a_d__uindex
		unique (word, area, range_date)
);

