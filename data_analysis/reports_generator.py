#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'reports_generator.py'

__author__ = 'kuoren'

import data_analysis.read_excel_util as excelUtil
import data_analysis.report as report


class ReportGenerator:
    def __init__(self, input_file, output_fold):
        self.input_file=input_file
        self.output_fold=output_fold
        pass
    
    @property
    def input_file(self):
        return self.input_file
    @property
    def output_fold(self):
        return self.output_fold
    
    def generate(self):
        '''v1'''
        data = excelUtil.read_excel(self.input_file)
        # 就业率和就业状态
        report.work_option_report(data, self.output_fold + '就业机会.xlsx')
        report.non_employee_report(data, self.output_fold + '未就业分析.xlsx')
        report.employee_report(data, self.output_fold + '就业率及就业就业状态.xlsx')
    
        # 就业竞争力
        report.major_relative_report(data, self.output_fold + '专业相关度.xlsx')
        report.job_meet_report(data, self.output_fold + '职业期待吻合度.xlsx')
    
        report.job_satisfy_report(data, self.output_fold + '就业满意度.xlsx')
        report.work_stability_report(data, self.output_fold + '工作稳定性.xlsx')
    
        report.income_report(data, self.output_fold + '月均收入.xlsx')
    
        # 就业分布
        report.employee_indurstry(data, self.output_fold + '就业行业分布.xlsx')
        report.employee_job(data, self.output_fold + '就业职业分布.xlsx')
        report.employee_industry_type(data, self.output_fold + '就业单位分布.xlsx')
        report.employee_industry_size(data, self.output_fold + '就业单位分布.xlsx')
        report.employee_region_report(data, self.output_fold + '就业地区分布.xlsx')
    
        # 求职过程与就业指导服务
        report.employee_difficult_report(data, self.output_fold + '求职过程.xlsx')
    
        # 母校综合评价
        report.school_satisfy_report(data, self.output_fold + '母校满意度.xlsx')
        report.school_recommed_report(data, self.output_fold + '母校推荐度.xlsx')
    
        # 学生指导与服务
        report.evelution_H4_Q_report(data, self.output_fold + '对学生生活服务的评价.xlsx')
        report.evelution_H4_P_report(data, self.output_fold + '对学生管理工作的评价.xlsx')
        report.evelution_H4_F_K_report(data, self.output_fold + '对就业教育服务的评价.xlsx')
        report.evelution_H4_L_O_report(data, self.output_fold + '对创业教育服务的反馈.xlsx')
    
        # 附加题
        report.evelution_H4_R_report(data, self.output_fold + '社团活动.xlsx')
        report.evelution_academic_report(data, self.output_fold + '母校学风认可度.xlsx')
        report.evelution_H4_T_report(data, self.output_fold + '教育教学总体评价.xlsx')
        report.evelution_H4_S_report(data, self.output_fold + '实践教学的评价.xlsx')
        report.evelution_H4_E_report(data, self.output_fold + '任课教师.xlsx')
    
        #国内升学
        report.report_report(data, self.output_fold + '国内升学.xlsx')
    
        # 出国境留学
        report.study_abroad_report(data, self.output_fold + '出国境留学.xlsx')
        # 自主创业
        report.self_employed_report(data, self.output_fold + '自主创业.xlsx')
        # 人才培养
        report.evelution_practice_report(data, self.output_fold + '对实践教学的评价.xlsx')
        report.evelution_lesson_report(data, self.output_fold + '对课堂教学的评价.xlsx')
        report.evelution_teach_report(data, self.output_fold + '对任课教师的评价.xlsx')
    
        # 特殊人群
        report.special_gender_report(data, self.output_fold + '不同性别.xlsx')
        report.special_education_report(data, self.output_fold + '教育行业和非教育行业.xlsx')
        report.special_origin_province_report(data, self.output_fold + '省内省外生源.xlsx')
        report.special_indurstry_province_report(data, self.output_fold + '省内省外就业.xlsx')
        report.special_national_report(data, self.output_fold + '汉族少数名族.xlsx')
    
        # 学习效果
        report.major_quality_report(data, self.output_fold + '专业素质.xlsx')
        report.basic_quality_report(data, self.output_fold + '基础素质.xlsx')

def generate_reports(input_file, output_folder):
    pass
