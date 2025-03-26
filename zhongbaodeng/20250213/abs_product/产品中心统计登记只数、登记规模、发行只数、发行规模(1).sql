--总体 登记只数 情况统计
select count(a.c_fundcode)
  FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m
 WHERE a.C_PDTTYPE=1 AND a.L_PDTTEMPLETID = 8 AND e.c_isregisterok=1 AND  a.c_fundcode = b.c_fundcode
   AND a.c_fundcode = c.c_fundcode
   AND c.c_mgrorgno = d.mem_code(+)
   AND a.c_fundcode = e.c_fundcode(+)
   AND a.c_fundcode = h.c_fundcode(+)
   AND h.c_trustee = m.mem_code(+)
   AND TO_CHAR(b.d_preregisterdate,'yyyy-mm-dd')>='2024-04-16' AND  TO_CHAR(b.d_preregisterdate,'yyyy-mm-dd')<='2024-04-16' ;

--总体 登记规模 情况统计
select sum(c.F_PRDREGBALA)
  FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m
 WHERE a.C_PDTTYPE=1 AND a.L_PDTTEMPLETID = 8 AND e.c_isregisterok=1 AND  a.c_fundcode = b.c_fundcode
   AND a.c_fundcode = c.c_fundcode
   AND c.c_mgrorgno = d.mem_code(+)
   AND a.c_fundcode = e.c_fundcode(+)
   AND a.c_fundcode = h.c_fundcode(+)
   AND h.c_trustee = m.mem_code(+)
   AND TO_CHAR(b.d_preregisterdate,'yyyy-mm-dd')>='2024-04-16' AND  TO_CHAR(b.d_preregisterdate,'yyyy-mm-dd')<='2024-04-16' ;


--根据受托人 登记只数 进行统计
select d.mem_name,count(d.mem_name)
  FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m
 WHERE a.C_PDTTYPE=1 AND a.L_PDTTEMPLETID = 8 AND e.c_isregisterok=1 AND  a.c_fundcode = b.c_fundcode
   AND a.c_fundcode = c.c_fundcode
   AND c.c_mgrorgno = d.mem_code(+)
   AND a.c_fundcode = e.c_fundcode(+)
   AND a.c_fundcode = h.c_fundcode(+)
   AND h.c_trustee = m.mem_code(+)
   AND TO_CHAR(b.d_preregisterdate,'yyyy-mm-dd')>='2024-04-16' AND  TO_CHAR(b.d_preregisterdate,'yyyy-mm-dd')<='2024-04-16' 
   GROUP BY  d.mem_name;



--根据托管银行 登记只数 行进行统计
select m.mem_name,count(m.mem_name)
  FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m
 WHERE a.C_PDTTYPE=1 AND a.L_PDTTEMPLETID = 8 AND e.c_isregisterok=1 AND  a.c_fundcode = b.c_fundcode
   and a.c_fundcode = c.c_fundcode
   and c.c_mgrorgno = d.mem_code(+)
   and a.c_fundcode = e.c_fundcode(+)
   and a.c_fundcode = h.c_fundcode(+)
   and h.c_trustee = m.mem_code(+)
   AND TO_CHAR(b.d_preregisterdate,'yyyy-mm-dd')>='2024-02-16' AND  TO_CHAR(b.d_preregisterdate,'yyyy-mm-dd')<='2024-04-16' 
   GROUP BY  m.mem_name;

--根据受托人 登记规模 进行统计
select d.mem_name,sum(c.F_PRDREGBALA)
  FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m
 WHERE a.C_PDTTYPE=1 AND a.L_PDTTEMPLETID = 8 AND e.c_isregisterok=1 AND  a.c_fundcode = b.c_fundcode
   AND a.c_fundcode = c.c_fundcode
   AND c.c_mgrorgno = d.mem_code(+)
   AND a.c_fundcode = e.c_fundcode(+)
   AND a.c_fundcode = h.c_fundcode(+)
   AND h.c_trustee = m.mem_code(+)
   AND TO_CHAR(b.d_preregisterdate,'yyyy-mm-dd')>='2024-04-16' AND  TO_CHAR(b.d_preregisterdate,'yyyy-mm-dd')<='2024-04-16' 
   GROUP BY  d.mem_name;



--根据托管银行 登记规模 行进行统计
select m.mem_name,sum(c.F_PRDREGBALA)
  FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m
 WHERE a.C_PDTTYPE=1 AND a.L_PDTTEMPLETID = 8 AND e.c_isregisterok=1 AND  a.c_fundcode = b.c_fundcode
   and a.c_fundcode = c.c_fundcode
   and c.c_mgrorgno = d.mem_code(+)
   and a.c_fundcode = e.c_fundcode(+)
   and a.c_fundcode = h.c_fundcode(+)
   and h.c_trustee = m.mem_code(+)
   AND TO_CHAR(b.d_preregisterdate,'yyyy-mm-dd')>='2024-02-16' AND  TO_CHAR(b.d_preregisterdate,'yyyy-mm-dd')<='2024-04-16' 
   GROUP BY  m.mem_name;
 
 
 --总体 发行只数 情况统计
select count(a.c_fundcode) 
   FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m,
       (select m.c_fundcode, m.c_stagefundcode, n.c_fundname as c_stagefundname, n.c_tafundcode as c_stagetafundcode
          FROM tpdtstagerelation m, tfundinfo n
         WHERE m.c_stagefundcode = n.c_fundcode) f
 WHERE a.L_PDTTEMPLETID = 8 AND (a.C_AUDITFLAG in(5,6,7,15,16,21,57,58)) AND  a.c_fundcode = b.c_fundcode
   and a.c_fundcode = c.c_fundcode
   and c.c_mgrorgno = d.mem_code(+)
   and a.c_fundcode = f.c_fundcode(+)
   and a.c_fundcode = e.c_fundcode(+)
   and a.c_fundcode = h.c_fundcode(+)
   and h.c_trustee = m.mem_code(+)
   AND TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')>='2025-02-08' AND  TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')<='2025-02-10'
   
 --获取产品代码、分级标识（0代表非分级，1代表分级）、分次标识（0代表非分次，1代表分次）
select a.c_fundcode,c.c_prdisclass,c.C_PRDISORDER 
   FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m,
       (select m.c_fundcode, m.c_stagefundcode, n.c_fundname as c_stagefundname, n.c_tafundcode as c_stagetafundcode
          FROM tpdtstagerelation m, tfundinfo n
         WHERE m.c_stagefundcode = n.c_fundcode) f
 WHERE a.L_PDTTEMPLETID = 8 AND (a.C_AUDITFLAG in(5,6,7,15,16,21,57,58)) AND  a.c_fundcode = b.c_fundcode
   and a.c_fundcode = c.c_fundcode
   and c.c_mgrorgno = d.mem_code(+)
   and a.c_fundcode = f.c_fundcode(+)
   and a.c_fundcode = e.c_fundcode(+)
   and a.c_fundcode = h.c_fundcode(+)
   and h.c_trustee = m.mem_code(+)
   AND TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')>='2024-02-08' AND  TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')<='2025-02-10'
   
--发行规模（c_prdisclass=0 && C_PRDISORDER=0）
SELECT F_BATCHFACTPAYBALA FROM tpdtbatchinfo o WHERE o.C_FUNDCODE = '';
--分级产品发行规模（c_prdisclass=1）
SELECT sum(F_CLASSFACTBALE) FROM TPDTPRDCLASSINFO o WHERE o.C_FUNDCODE = '';
--分次产品发行规模(C_PRDISORDER=1)
SELECT sum(F_ORDERFACTCOLLECTBALA) FROM TPDTORDERINFO o WHERE o.C_FUNDCODE = '';

   
--根据受托人 发行只数 情况统计
select d.mem_name,count(d.mem_name)
   FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m,
       (select m.c_fundcode, m.c_stagefundcode, n.c_fundname as c_stagefundname, n.c_tafundcode as c_stagetafundcode
          FROM tpdtstagerelation m, tfundinfo n
         WHERE m.c_stagefundcode = n.c_fundcode) f
 WHERE a.L_PDTTEMPLETID = 8 AND (a.C_AUDITFLAG in(5,6,7,15,16,21,57,58)) AND  a.c_fundcode = b.c_fundcode
   and a.c_fundcode = c.c_fundcode
   and c.c_mgrorgno = d.mem_code(+)
   and a.c_fundcode = f.c_fundcode(+)
   and a.c_fundcode = e.c_fundcode(+)
   and a.c_fundcode = h.c_fundcode(+)
   and h.c_trustee = m.mem_code(+)
   AND TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')>='2025-02-08' AND  TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')<='2025-02-10'
   GROUP BY  d.mem_name;

--根据托管银行  发行只数 情况统计
select m.mem_name,count(m.mem_name)
   FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m,
       (select m.c_fundcode, m.c_stagefundcode, n.c_fundname as c_stagefundname, n.c_tafundcode as c_stagetafundcode
          FROM tpdtstagerelation m, tfundinfo n
         WHERE m.c_stagefundcode = n.c_fundcode) f
 WHERE a.L_PDTTEMPLETID = 8 AND (a.C_AUDITFLAG in(5,6,7,15,16,21,57,58)) AND  a.c_fundcode = b.c_fundcode
   and a.c_fundcode = c.c_fundcode
   and c.c_mgrorgno = d.mem_code(+)
   and a.c_fundcode = f.c_fundcode(+)
   and a.c_fundcode = e.c_fundcode(+)
   and a.c_fundcode = h.c_fundcode(+)
   and h.c_trustee = m.mem_code(+)
   AND TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')>='2025-02-08' AND  TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')<='2025-02-10'
   GROUP BY  m.mem_name;


--查询受托人发行规模
--查询受托人机构号
select DISTINCT c.c_mgrorgno,d.mem_name
   FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m,
       (select m.c_fundcode, m.c_stagefundcode, n.c_fundname as c_stagefundname, n.c_tafundcode as c_stagetafundcode
          FROM tpdtstagerelation m, tfundinfo n
         WHERE m.c_stagefundcode = n.c_fundcode) f
 WHERE a.L_PDTTEMPLETID = 8 AND (a.C_AUDITFLAG in(5,6,7,15,16,21,57,58)) AND  a.c_fundcode = b.c_fundcode
   and a.c_fundcode = c.c_fundcode
   and c.c_mgrorgno = d.mem_code(+)
   and a.c_fundcode = f.c_fundcode(+)
   and a.c_fundcode = e.c_fundcode(+)
   and a.c_fundcode = h.c_fundcode(+)
   and h.c_trustee = m.mem_code(+)
   AND TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')>='2025-02-08' AND  TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')<='2025-02-10';

 --获取产品代码、分级标识（0代表非分级，1代表分级）、分次标识（0代表非分次，1代表分次），增加受托人查询条件(c_mgrorgno 的值)
select a.c_fundcode,c.c_prdisclass,c.C_PRDISORDER 
   FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m,
       (select m.c_fundcode, m.c_stagefundcode, n.c_fundname as c_stagefundname, n.c_tafundcode as c_stagetafundcode
          FROM tpdtstagerelation m, tfundinfo n
         WHERE m.c_stagefundcode = n.c_fundcode) f
 WHERE a.L_PDTTEMPLETID = 8 AND (a.C_AUDITFLAG in(5,6,7,15,16,21,57,58)) AND  a.c_fundcode = b.c_fundcode
   and a.c_fundcode = c.c_fundcode
   and c.c_mgrorgno = d.mem_code(+)
   and a.c_fundcode = f.c_fundcode(+)
   and a.c_fundcode = e.c_fundcode(+)
   and a.c_fundcode = h.c_fundcode(+)
   and h.c_trustee = m.mem_code(+)
   AND c.c_mgrorgno = ?
   AND TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')>='2024-02-08' AND  TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')<='2025-02-10'

--查询托管银行发行规模
--查询托管银行机构号
select DISTINCT h.c_trustee,m.mem_name
   FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m,
       (select m.c_fundcode, m.c_stagefundcode, n.c_fundname as c_stagefundname, n.c_tafundcode as c_stagetafundcode
          FROM tpdtstagerelation m, tfundinfo n
         WHERE m.c_stagefundcode = n.c_fundcode) f
 WHERE a.L_PDTTEMPLETID = 8 AND (a.C_AUDITFLAG in(5,6,7,15,16,21,57,58)) AND  a.c_fundcode = b.c_fundcode
   and a.c_fundcode = c.c_fundcode
   and c.c_mgrorgno = d.mem_code(+)
   and a.c_fundcode = f.c_fundcode(+)
   and a.c_fundcode = e.c_fundcode(+)
   and a.c_fundcode = h.c_fundcode(+)
   and h.c_trustee = m.mem_code(+)
   AND TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')>='2025-02-08' AND  TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')<='2025-02-10';

 --获取产品代码、分级标识（0代表非分级，1代表分级）、分次标识（0代表非分次，1代表分次），增加托管银行查询条件(c_trustee 的值)
select a.c_fundcode,c.c_prdisclass,c.C_PRDISORDER 
   FROM tfundinfo a,
       tpdtoperateinfo b,
       tpdtbasicinfo c,
       member.member_info d,
       tpdtextendinfo e,
       tpdtbatchinfo h,
       member.member_info m,
       (select m.c_fundcode, m.c_stagefundcode, n.c_fundname as c_stagefundname, n.c_tafundcode as c_stagetafundcode
          FROM tpdtstagerelation m, tfundinfo n
         WHERE m.c_stagefundcode = n.c_fundcode) f
 WHERE a.L_PDTTEMPLETID = 8 AND (a.C_AUDITFLAG in(5,6,7,15,16,21,57,58)) AND  a.c_fundcode = b.c_fundcode
   and a.c_fundcode = c.c_fundcode
   and c.c_mgrorgno = d.mem_code(+)
   and a.c_fundcode = f.c_fundcode(+)
   and a.c_fundcode = e.c_fundcode(+)
   and a.c_fundcode = h.c_fundcode(+)
   and h.c_trustee = m.mem_code(+)
   AND h.c_trustee = ?
   AND TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')>='2025-02-08' AND  TO_CHAR(b.d_accessstoredate,'yyyy-mm-dd')<='2025-02-10'