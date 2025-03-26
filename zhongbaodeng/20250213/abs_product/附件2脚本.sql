--资产支持计划登记情况
SELECT
	a.C_TAFUNDCODE,
	--产品名称
	a.C_FUNDNAME,
	--管理人
	d.mem_name,
	--登记规模
	b.F_PRDREGBALA,
	--基础资产类型 3734
	c.C_INFRACLASS,
	--登记日期
	e.d_preregisterdate,
	--登记状态
	'予以登记' 
FROM
	tfundinfo a,
	TPDTBASICINFO b,
	TPDTINFRAINFO c,
	member.member_info d,
	tpdtoperateinfo e
WHERE
	a.c_fundcode = b.c_fundcode(+)
AND a.c_fundcode = c.c_fundcode(+)
AND b.c_mgrorgno = d.mem_code(+)
AND a.c_fundcode = e.c_fundcode(+)
AND a.C_PDTTYPE = 1 
AND a.L_PDTTEMPLETID = 8 
AND a.C_AUDITFLAG in (3,4,5,6,7,12,13,15,16,20,21,22,25,29,55,56,57,58)
ORDER BY e.D_PREREGISTERDATE DESC NULLS LAST;

--字典项查询语句
select c_sysname, l_keyno, c_keyvalue, c_caption, c_modify, c_memo, c_english, l_order from tdictionary where l_keyno = 3734 order by c_keyvalue;

--报送日期查询
SELECT
	END_
FROM
	(
		SELECT
			T.END_
		FROM
			jbpm4_ext_hist_task E,
			jbpm4_hist_task T,
			jbpm4_hist_procinst P
		WHERE
			E.dbid_ = T.dbid_
		AND T.procinst_ = P.dbid_
		AND E.biz_flow_uuid_ = (
			SELECT
				f.c_fundcode
			FROM
				tfundinfo f
			WHERE
				f.c_Tafundcode = '上一步查询出来的C_TAFUNDCODE值'
		)
		AND P.proc_exe_name_ = '产品登记流程'
		AND E.EXTFIELD1 = '机构复核通过'
		AND T.outcome_ = 'pass'
		ORDER BY
			T.END_
	)
WHERE
	ROWNUM = 1;
	
	
--组合资管产品明细
SELECT
	a.C_TAFUNDCODE,
		a.C_FUNDNAME,--产品名称
		c.C_PRDTYPE,--产品类型    数据字典编号 5024
		a.C_OPERATEWAY,--运作方式 数据字典编号  5132
		b.C_REGISTERCLASSIY,--登记方式 数据字典编号 9031
		'予以登记'--流程进度
	FROM
		tfundinfo a,
		TPDTEXTENDINFO b,
		TPDTBASICINFO c
	WHERE
		a.c_fundcode = b.c_fundcode(+)
		AND a.c_fundcode = c.c_fundcode(+)
		AND a.C_AUDITFLAG in(32,45,46,47,50,51,52,53,54)
		AND a.L_PDTTEMPLETID in(10,17);


--按照 产品类型 进行统计
SELECT
	c.C_PRDTYPE,COUNT(c.C_PRDTYPE) 
	FROM
		tfundinfo a,
		TPDTEXTENDINFO b,
		TPDTBASICINFO c,
		tpdtoperateinfo d
	WHERE
		a.c_fundcode = b.c_fundcode(+)
		AND a.c_fundcode = c.c_fundcode(+)
		AND a.c_fundcode = d.c_fundcode(+)
		AND a.C_AUDITFLAG in(32,45,46,47,50,51,52,53,54)
		AND a.L_PDTTEMPLETID in(10,17)
		AND TO_CHAR(d.d_preregisterdate,'yyyy-mm-dd')>='2024-04-16' AND  TO_CHAR(d.d_preregisterdate,'yyyy-mm-dd')<='2024-12-16'
GROUP BY c.C_PRDTYPE;


--按照 运作方式 进行统计
SELECT
	a.C_OPERATEWAY,COUNT(a.C_OPERATEWAY) 
	FROM
		tfundinfo a,
		TPDTEXTENDINFO b,
		TPDTBASICINFO c,
		tpdtoperateinfo d
	WHERE
		a.c_fundcode = b.c_fundcode(+)
		AND a.c_fundcode = c.c_fundcode(+)
		AND a.c_fundcode = d.c_fundcode(+)
		AND a.C_AUDITFLAG in(32,45,46,47,50,51,52,53,54)
		AND a.L_PDTTEMPLETID in(10,17)
		AND TO_CHAR(d.d_preregisterdate,'yyyy-mm-dd')>='2024-04-16' AND  TO_CHAR(d.d_preregisterdate,'yyyy-mm-dd')<='2024-12-16'
GROUP BY a.C_OPERATEWAY;

--按照 产品管理人、产品类型 进行统计
SELECT
	e.mem_name,c.C_PRDTYPE,COUNT(c.C_PRDTYPE) 
	FROM
		tfundinfo a,
		TPDTEXTENDINFO b,
		TPDTBASICINFO c,
		tpdtoperateinfo d,
		member.member_info e
	WHERE
		a.c_fundcode = b.c_fundcode(+)
		AND a.c_fundcode = c.c_fundcode(+)
		and c.c_mgrorgno = e.mem_code(+)
		AND a.c_fundcode = d.c_fundcode(+)
		AND a.C_AUDITFLAG in(32,45,46,47,50,51,52,53,54)
		AND a.L_PDTTEMPLETID in(10,17)
		AND TO_CHAR(d.d_preregisterdate,'yyyy-mm-dd')>='2024-04-16' AND  TO_CHAR(d.d_preregisterdate,'yyyy-mm-dd')<='2024-12-16'
GROUP BY e.mem_name,c.C_PRDTYPE
ORDER BY e.mem_name;


--按照 产品管理人、运作方式 进行统计
SELECT
	e.mem_name,a.C_OPERATEWAY,COUNT(a.C_OPERATEWAY) 
	FROM
		tfundinfo a,
		TPDTEXTENDINFO b,
		TPDTBASICINFO c,
		tpdtoperateinfo d,
		member.member_info e
	WHERE
		a.c_fundcode = b.c_fundcode(+)
		AND a.c_fundcode = c.c_fundcode(+)
		and c.c_mgrorgno = e.mem_code(+)
		AND a.c_fundcode = d.c_fundcode(+)
		AND a.C_AUDITFLAG in(32,45,46,47,50,51,52,53,54)
		AND a.L_PDTTEMPLETID in(10,17)
		AND TO_CHAR(d.d_preregisterdate,'yyyy-mm-dd')>='2024-04-16' AND  TO_CHAR(d.d_preregisterdate,'yyyy-mm-dd')<='2024-12-16'
GROUP BY e.mem_name,a.C_OPERATEWAY;


