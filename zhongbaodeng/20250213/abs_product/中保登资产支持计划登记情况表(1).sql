-- 总体
SELECT
	sum(a.f_lastshares * b.price)
FROM
	(
	SELECT
		a.c_fundacco,
		a.c_fundcode,
		to_char(a.d_cdate, 'yyyymmdd') d_cdate,
		a.f_occurshares,
		a.f_lastshares,
		to_char(a.d_requestdate, 'yyyymmdd') d_date,
		ROW_NUMBER() OVER (PARTITION BY a.c_fundacco,a.c_fundcode ORDER BY to_char(a.d_requestdate, 'yyyymmdd') desc,a.C_CSERIALNO desc) AS rn
	FROM
		tsharecurrents a
	WHERE
		a.C_OUTBUSINFLAG  NOT IN ('031','032') and
		to_char(a.d_cdate, 'yyyymmdd') <= '截止日期' ) a ,
	(
	SELECT
			c_bondcode fundcode,
			C_BONDFULLNAME fundname,
			c_mgrcode,
			c_producttype producttype,
			f_issueprice price
	FROM
			tbondinfo a
	WHERE
 a.c_producttype = '3' ) b
WHERE
	a.rn = 1
	AND a.c_fundcode = b.fundcode;
	
-- 受托管理人维度
SELECT
   c.c_memname,
	sum(a.f_lastshares * b.price)
FROM
	(
	SELECT
		a.c_fundacco,
		a.c_fundcode,
		to_char(a.d_cdate, 'yyyymmdd') d_cdate,
		a.f_occurshares,
		a.f_lastshares,
		to_char(a.d_requestdate, 'yyyymmdd') d_date,
		ROW_NUMBER() OVER (PARTITION BY a.c_fundacco,a.c_fundcode ORDER BY to_char(a.d_requestdate, 'yyyymmdd') desc,a.C_CSERIALNO desc) AS rn
	FROM
		tsharecurrents a
	WHERE
		a.C_OUTBUSINFLAG  NOT IN ('031','032') and
		to_char(a.d_cdate, 'yyyymmdd') <= '截止日期' ) a ,
	(
	SELECT
			c_bondcode fundcode,
			C_BONDFULLNAME fundname,
			c_mgrcode,
			c_producttype producttype,
			f_issueprice price
	FROM
			tbondinfo a
	WHERE
		 a.c_producttype = '3' ) b,
	(
	SELECT
		a.c_custno c_fundacco,
		m.c_memname c_memname
	FROM
		tcustomerinfo a ,
		tmemberinfo m
	WHERE
 a.c_custodiancode = m.c_memcode
) c
WHERE
		a.rn = 1
	AND a.c_fundcode = b.fundcode
	AND a.c_fundacco = c.c_fundacco
	GROUP BY c.c_memname;

-- 产品管理人维度
SELECT
b.c_memname,
	sum(a.f_lastshares * b.price)
FROM
	(
	SELECT
		a.c_fundacco,
		a.c_fundcode,
		to_char(a.d_cdate, 'yyyymmdd') d_cdate,
		a.f_occurshares,
		a.f_lastshares,
		to_char(a.d_requestdate, 'yyyymmdd') d_date,
		ROW_NUMBER() OVER (PARTITION BY a.c_fundacco,a.c_fundcode ORDER BY to_char(a.d_requestdate, 'yyyymmdd') desc,a.C_CSERIALNO desc) AS rn
	FROM
		tsharecurrents a
	WHERE
		a.C_OUTBUSINFLAG  NOT IN ('031','032') and
		to_char(a.d_cdate, 'yyyymmdd') <= '截止日期' ) a ,
	(
	SELECT
			c_bondcode fundcode,
			C_BONDFULLNAME fundname,
			c_mgrcode,
			c_producttype producttype,
			f_issueprice price,
		m.c_memname c_memname
	FROM
			tbondinfo a,tmemberinfo m
	WHERE
		a.c_mgrcode = m.c_memcode
		AND a.c_producttype = '3' ) b
WHERE
		a.rn = 1
	AND a.c_fundcode = b.fundcode
	GROUP BY b.c_memname;