import pymysql,pymongo

class Isecd(object):
    def __init__(self):
        pass

    def stucount(self,starttime,endtime='',listname='',subjectname='',teachername='',classname=''):
        self.starttime=starttime
        self.endtime=endtime
        self.listname=listname
        self.subjectname=subjectname
        self.teachername=teachername
        self.classname=classname
        conn = pymysql.connect(host='10.4.3.6', port=4417, user='root', passwd='jfkj@2019', db='jf_ispaas')
        cur = conn.cursor()
        sql = """
            SELECT sum(t.maxnum)/sum(t.Stunum) FROM(
            SELECT avg(c.max_num) maxnum,b.Stunum Stunum FROM jf_rcurs a
            JOIN jf_curriculums b ON a.Uid=b.CurClaId
            JOIN cid_count_job_b c ON a.Uid_b=c.cur_all_id
            JOIN jf_placeinfo d ON a.ClassroomID=d.PlaceId
            WHERE  a.`status`='A' AND a.ifstudy=1 
            AND b.`Status`='A' AND d.`status`='A'  AND c.max_num>=0 
        """
        sql1 = """
            GROUP BY c.cur_all_id)t
        """
        if self.endtime == '':
            sql = sql + '\t' + "AND a.actureDate='%s'" % (self.starttime)
        else:
            sql = sql + '\t' + "AND a.actureDate BETWEEN '%s' AND '%s'" % (self.starttime,self.endtime)
        if self.listname != '':
            sql = sql + '\t' + "AND b.Grd_Listname='%s'"%(self.listname)
        if self.subjectname != '':
            sql = sql + '\t' + "AND b.SubjectName='%s'" % (self.subjectname)
        if self.teachername != '':
            sql = sql + '\t' + "AND b.TeacherName='%s'" % (self.teachername)
        if self.classname != '':
            sql = sql + '\t' + "AND b.CurClassName='%s'" % (self.classname)

        sql = sql + '\t' + sql1
        cur.execute(sql)
        result = str(round(cur.fetchall()[0][0]*100,2))+'%'
        cur.close()
        conn.close()
        return result
    def stucountdetail(self,starttime,endtime,listId='',subjectId='',teacherId='',lessnum='',countmin='',countmax=''):
        self.starttime=starttime
        self.endtime=endtime
        self.listId=listId
        self.subjectId=subjectId
        self.teacherId=teacherId
        self.lessnum=lessnum
        self.countmin=countmin
        self.countmax=countmax
        if self.countmin is None:
            self.countmin = ''
        if self.countmax is None:
            self.countmax = ''
        conn = pymysql.connect(host='10.4.3.6', port=4417, user='root', passwd='jfkj@2019', db='jf_ispaas')
        cur = conn.cursor()
        sql = """
            SELECT GROUP_CONCAT(distinct b.Grd_Listname),concat(e.place_name,d.pla_name),b.Type,b.SubjectName,b.TeacherName,CONCAT(a.actureDate,' 第',a.ctsort,'节') '时间',
            IF(floor(avg(c.max_num))=-1,'--',CONCAT(ROUND(avg(c.max_num)*100/b.Stunum,0),'%')),b.Stunum,IF(floor(avg(c.max_num))=-1,'--',floor(avg(c.max_num))) '实到人数' 
            FROM jf_rcurs_b a
            JOIN jf_curriculums b ON a.Uid=b.CurClaId_B
            JOIN cid_count_job_b c ON a.Uid=c.cur_all_id
            JOIN jf_placeinfo d ON a.ClassroomID=d.PlaceId
            JOIN jf_place_tree e ON d.tree_id=e.Puid
            JOIN jf_rcurs f ON a.Uid=f.Uid_b
            WHERE  a.`status`='A' AND a.ifstudy=1 
            AND b.`Status`='A' AND d.`status`='A'
        """ + '\t' "AND a.actureDate BETWEEN '%s' AND '%s'"%(self.starttime,self.endtime)
        sql1 = """
            GROUP BY c.cur_all_id
        """
        sql2 = """
            ORDER BY avg(c.max_num)/b.Stunum
        """
        if self.listId != '':
            sql = sql + '\t' + "AND b.Grd_Id='%s'"%(self.listId)
        if self.subjectId != '':
            sql = sql + '\t' + "AND b.SubjectID='%s'" % (self.subjectId)
        if self.teacherId != '':
            sql = sql + '\t' + "AND b.TeacherID='%s'" % (self.teacherId)
        if self.lessnum != '':
            sql = sql + '\t' + "AND f.lessonOrderNum='%s'" % (self.lessnum)

        sql = sql + '\t' + sql1

        if self.countmin != '' and self.countmax != '':
            sql = sql + '\t' + "HAVING (avg(c.max_num)*100/b.Stunum) BETWEEN '%s' AND '%s'" % (self.countmin,self.countmax)
        sql = sql + '\t' + sql2

        print("查询sql：" + "\n" + str(sql))
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
