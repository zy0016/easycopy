--产品发行规模统计
SELECT
	b.fundcode,
	sum(a.f_occurshares * b.price)
FROM
	(
	SELECT
		a.c_fundacco,
		a.c_fundcode,
		to_char(a.d_cdate, 'yyyymmdd') d_cdate,
		a.f_occurshares,
		a.f_lastshares,
		to_char(a.d_requestdate, 'yyyymmdd') d_date,
		a.c_outbusinflag
	FROM
		tsharecurrents a
	WHERE
		a.c_outbusinflag = '130'
		AND to_char(a.d_requestdate, 'yyyymmdd') >= '20231001'
		AND to_char(a.d_requestdate, 'yyyymmdd') <= '20250213' ) a ,
	(
	SELECT
			c_bondcode fundcode,
			c_producttype producttype,
			f_issueprice price
	FROM
			tbondinfo a
	WHERE
		a.c_producttype = '3' ) b
WHERE
	a.c_fundcode = b.fundcode
GROUP BY
	b.fundcode;

--产品兑付规模统计（c_outbusinflag业务类型需与生产再验证一下）	
SELECT
	b.fundcode,
	sum(a.f_occurshares * b.price)
FROM
	(
	SELECT
		a.c_fundacco,
		a.c_fundcode,
		to_char(a.d_cdate, 'yyyymmdd') d_cdate,
		a.f_occurshares,
		a.f_lastshares,
		to_char(a.d_requestdate, 'yyyymmdd') d_date,
		a.c_outbusinflag
	FROM
		tsharecurrents a
	WHERE
		a.c_outbusinflag = '142'
		AND to_char(a.d_requestdate, 'yyyymmdd') >= '20231001'
		AND to_char(a.d_requestdate, 'yyyymmdd') <= '20250213' ) a ,
	(
	SELECT
			c_bondcode fundcode,
			c_producttype producttype,
			f_issueprice price
	FROM
			tbondinfo a
	WHERE
		a.c_producttype = '3' ) b
WHERE
	a.c_fundcode = b.fundcode
GROUP BY
	b.fundcode;