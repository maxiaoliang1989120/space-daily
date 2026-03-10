#!/usr/bin/env python3
"""
Space Daily - 空天信息日报生成器
生成包含商业航天、低空经济、遥感卫星的每日行业日报
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path

class SpaceDailyGenerator:
    def __init__(self):
        self.template_dir = Path(__file__).parent.parent / "templates"
        self.output_dir = Path(__file__).parent.parent / "docs"
        self.output_dir.mkdir(exist_ok=True)
        
    def get_date_info(self):
        """获取日期信息"""
        today = datetime.now()
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return {
            "date": today.strftime("%Y年%m月%d日"),
            "weekday": weekdays[today.weekday()],
            "datetime": today.strftime("%Y-%m-%d %H:%M")
        }
    
    def fetch_news(self):
        """
        获取新闻数据（模拟数据，实际部署时替换为真实API/RSS抓取）
        """
        # 模拟今日新闻数据
        news_data = {
            "commercial": [
                {
                    "title": "SpaceX星舰第8次试飞成功完成静态点火测试",
                    "summary": "SpaceX宣布星舰Super Heavy助推器成功完成静态点火测试，为即将到来的第8次轨道试飞做准备。本次测试持续约10秒，所有33台猛禽发动机正常工作。",
                    "source": "SpaceNews",
                    "time": "2小时前",
                    "priority": "high",
                    "tags": ["商业航天", "SpaceX", "星舰"]
                },
                {
                    "title": "蓝箭航天朱雀三号完成200吨级液氧甲烷发动机长程试车",
                    "summary": "蓝箭航天宣布朱雀三号运载火箭配套的200吨级液氧甲烷发动机完成500秒长程试车，标志着可回收火箭技术取得重要突破。",
                    "source": "泰伯网",
                    "time": "4小时前",
                    "priority": "high",
                    "tags": ["商业航天", "蓝箭航天", "朱雀三号"]
                },
                {
                    "title": "天兵科技天龙三号首飞进入倒计时",
                    "summary": "天兵科技宣布天龙三号大型液体运载火箭完成总装出厂评审，计划6月首飞，对标SpaceX猎鹰9号，具备一子级垂直回收能力。",
                    "source": "36氪",
                    "time": "6小时前",
                    "priority": "medium",
                    "tags": ["商业航天", "天兵科技"]
                }
            ],
            "low_altitude": [
                {
                    "title": "亿航智能获得沙特100架EH216-S订单",
                    "summary": "亿航智能与沙特 frontline 投资集团签署战略合作协议，获得100架EH216-S无人驾驶载人航空器订单，用于空中交通和旅游业。",
                    "source": "亿航智能",
                    "time": "1小时前",
                    "priority": "high",
                    "tags": ["低空经济", "eVTOL", "亿航智能"]
                },
                {
                    "title": "民航局发布《民用无人驾驶航空发展路线图》修订意见稿",
                    "summary": "民航局就《民用无人驾驶航空发展路线图》修订征求意见，提出到2030年形成万亿级低空经济市场规模目标。",
                    "source": "民航局",
                    "time": "3小时前",
                    "priority": "high",
                    "tags": ["低空经济", "政策法规", "无人机"]
                },
                {
                    "title": "小鹏汇天旅航者X2完成深圳CBD区域飞行演示",
                    "summary": "小鹏汇天旅航者X2无人驾驶载人航空器在深圳福田CBD完成飞行演示，标志着城市空中交通(UAM)场景应用取得新进展。",
                    "source": "小鹏汇天",
                    "time": "5小时前",
                    "priority": "medium",
                    "tags": ["低空经济", "eVTOL", "小鹏汇天"]
                }
            ],
            "remote": [
                {
                    "title": "中科星图发布星图低空云V1.0",
                    "summary": "中科星图正式发布星图低空云V1.0，融合数字地球、人工智能、空天信息技术，实现低空活动三维仿真、航线智能规划、交通协同管理等核心能力。",
                    "source": "中科星图",
                    "time": "2小时前",
                    "priority": "high",
                    "tags": ["遥感卫星", "低空经济", "中科星图"]
                },
                {
                    "title": "航天宏图女娲星座首颗雷达卫星成功入轨",
                    "summary": "航天宏图自主研发的女娲星座首颗雷达遥感卫星成功发射入轨，标志着国内首个商业雷达卫星星座建设启动。",
                    "source": "航天宏图",
                    "time": "4小时前",
                    "priority": "high",
                    "tags": ["遥感卫星", "SAR", "航天宏图"]
                },
                {
                    "title": "Planet Labs发布新一代Pelican高分辨率卫星首批图像",
                    "summary": "Planet Labs发布Pelican-1卫星首批30厘米分辨率图像，展示了对车辆、建筑等细节的高清成像能力。",
                    "source": "Planet Labs",
                    "time": "8小时前",
                    "priority": "medium",
                    "tags": ["遥感卫星", "Planet Labs"]
                }
            ],
            "investment": [
                {
                    "title": "低空经济赛道Q1融资超50亿元",
                    "summary": "据统计，2025年第一季度eVTOL及低空经济领域融资超50亿元，沃飞长空、时的科技等头部企业完成B轮及以后融资。",
                    "source": "投中网",
                    "time": "3小时前",
                    "priority": "medium",
                    "tags": ["投融资", "低空经济", "eVTOL"]
                },
                {
                    "title": "银河航天完成新一轮融资，估值超120亿元",
                    "summary": "银河航天完成新一轮融资，投后估值超120亿元，资金将用于卫星互联网星座建设和海外业务拓展。",
                    "source": "36氪",
                    "time": "5小时前",
                    "priority": "medium",
                    "tags": ["投融资", "卫星互联网", "银河航天"]
                }
            ],
            "policy": [
                {
                    "title": "低空经济首次写入国务院政府工作报告",
                    "summary": "2024年全国两会正式将低空经济列为战略性新兴产业，深圳、广州、合肥、成都等地密集出台低空飞行管理办法。",
                    "source": "新华社",
                    "time": "今日",
                    "priority": "high",
                    "tags": ["政策法规", "低空经济"]
                }
            ],
            "tech": [
                {
                    "title": "Vision Mamba在遥感领域应用综述发表",
                    "summary": "最新综述论文《Vision Mamba in Remote Sensing》发表，系统梳理了Mamba架构在遥感影像分类、变化检测等任务中的应用进展。",
                    "source": "arXiv",
                    "time": "6小时前",
                    "priority": "medium",
                    "tags": ["技术前沿", "AI", "Mamba"]
                }
            ]
        }
        return news_data
    
    def render_news_item(self, news):
        """渲染单条新闻"""
        priority_class = f"priority-{news.get('priority', 'medium')}"
        tag_html = ''.join([f'<span class="tag tag-{self.get_tag_class(tag)}">{tag}</span>' for tag in news.get('tags', [])])
        
        return f'''
        <div class="news-item {priority_class}">
            <div class="news-header">
                <div class="news-title">{news['title']}</div>
            </div>
            <div class="news-meta">{tag_html}</div>
            <div class="news-summary">{news['summary']}</div>
            <div class="news-footer">
                <span>{news['source']} · {news['time']}</span>
                <a href="#" class="news-link">查看详情 →</a>
            </div>
        </div>
        '''
    
    def get_tag_class(self, tag):
        """获取标签样式类"""
        tag_map = {
            "商业航天": "commercial",
            "低空经济": "lowaltitude",
            "遥感卫星": "remote",
            "投融资": "investment",
            "政策法规": "policy",
            "技术前沿": "tech"
        }
        return tag_map.get(tag, "commercial")
    
    def generate(self):
        """生成日报"""
        # 读取模板
        template_path = self.template_dir / "index-v2.html"
        template = template_path.read_text(encoding='utf-8')
        
        # 获取数据
        date_info = self.get_date_info()
        news_data = self.fetch_news()
        
        # 渲染各板块
        sections = {}
        category_map = {
            "commercial": "COMMERCIAL",
            "low_altitude": "LOWALTITUDE",
            "remote": "REMOTE",
            "investment": "INVESTMENT",
            "policy": "POLICY",
            "tech": "TECH"
        }
        for category, news_list in news_data.items():
            key_prefix = category_map.get(category, category.upper())
            sections[f"{key_prefix}_NEWS"] = ''.join([self.render_news_item(n) for n in news_list])
            sections[f"{key_prefix}_COUNT"] = str(len(news_list))
        
        sections["TOTAL_COUNT"] = str(sum(len(v) for v in news_data.values()))
        
        # 替换模板变量
        html = template
        html = html.replace("{{DATE}}", date_info["date"])
        html = html.replace("{{WEEKDAY}}", date_info["weekday"])
        html = html.replace("{{DATETIME}}", date_info["datetime"])
        
        for key, value in sections.items():
            html = html.replace(f"{{{{{key}}}}}", value)
            # 同时尝试替换双花括号格式
            html = html.replace(f"{{{{{key}}}}}", value)
        
        # 保存文件
        output_file = self.output_dir / "index.html"
        output_file.write_text(html, encoding='utf-8')
        
        print(f"✅ 日报生成成功: {output_file}")
        print(f"📅 日期: {date_info['date']}")
        print(f"📊 共 {sections['TOTAL_COUNT']} 条资讯")
        
        return output_file

if __name__ == "__main__":
    generator = SpaceDailyGenerator()
    generator.generate()
