-- login.sql
-- written: 2019.4.03
--    - update: 2019.4.06
--
set pagesize 100 linesize 130
col report format a400
-- def _editor=notepad++

-- Tables: Employee & Dept
col EmpNo    format 99999
col EName    format a12
col Job      format a14
col Mgr      format 9999
col HireDate format a12
col Sal      format 999,999
col comm     format 999,999

col DeptNo   format 99999
col DName    format a14
col Loc      format a13

col Grade    format 999999
col LoSal    format 999999
col HiSal    format 999999
             
-- Tables: K-league tables
col Player_ID     format a8    heading Player|ID
-- col Player_ID     heading Player|ID   format a8    # ???
col Player_Name   format a12   heading Player|Name  
col E_Player_Name format a10   heading Player|E.Name
col NickName      format a20
col Join_yyyy     format a6    heading Join|YYYY
col Position      format a6    heading Posi|tion
col Back_No       format 999   heading Back|No
col Nation        format a12
col Birth_Date    format a8    heading Birth|date
col solar         format a5
col Height        format 999
col Weight        format 999

col Team_ID       format a7    heading Team|ID
col Region_Name   format a8    heading Region|Name
col Team_Name     format a20   heading Team|Name
col E_Team_Name   format a20   heading Team|E.Name
col Orig_yyyy     format a8    heading Orig|YYYY
col Owner         format a10

col Stadium_ID    format a6    heading Stadium|ID
col STADIUM_NAME  format a20   heading Stadium|Name
col SEAT_COUNT    format 99999 heading Seat|Count
col address       format a40
col DDD           format a3
col TEL           format a10 

col SCHE_DATE     format a8
col GUBUN         format 5
col HOMETEAM_ID   format a7    heading Home|Team_ID
col AWAYTEAM_ID   format a7    heading AWAY|Team_ID
col HOME_SCORE    format 9999  heading Home|Score
col AWAY_SCORE    format 9999  heading AWAY|Score

-- Oracle Dictionary Tablesselt
-- TAB
col TNAME         format a35
col TABTYPE       format a10
col CLUSTERID     format a10

-- ALL_USERS & DBA_USERS
col USERNAME      format a14
col USER_ID       format 99999999
col CREATED       format a8
col ACCOUNT_STATUS  format a9      heading Account|Status

--
col ACCOUNT       format a14
col LOCK_DATE     format a9    heading Lock|Date
col EXPIRY_DATE   format a9    heading Expiry|Date
col CREATED       format a9

--set sqlprompt "&user> "
set sqlprompt "_user> "
alter session set NLS_DATE_FORMAT='YYYY-MON-DD'

-- setting Envornment Variables
set FEEDBACK ON
set LINESIZE 130
set TERM ON
set TIMING ON
-- SET TERMOUT ON
-- SET TAB OFF
-- SET TRIM ON
-- SET TRIMSPOOL ON
