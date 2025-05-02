# -*- coding: utf-8 -*-
"""
Created on Fri May  2 10:54:48 2025

@author: CHEN
"""

import json
import os
# 系统配置
CONFIG = {
    'data_file': 'attendees_data.json',
    'allowed_tickets': ['VIP', '普通票', '学生票'],
    'min_age': {
        '普通票': 18,
        '学生票': 16
    }
}

def clear_screen():
    """清空控制台屏幕"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    """显示系统标题"""
    print("="*50)
    print("      音乐会入场资格审核系统".center(40))
    print("="*50)
    print()

def load_data():
    """加载历史数据"""
    try:
        with open(CONFIG['data_file'], 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """保存数据到文件"""
    with open(CONFIG['data_file'], 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_valid_input(prompt, input_type=str, valid_options=None):
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                raise ValueError("输入不能为空")
            
            # 类型转换
            if input_type == int:
                user_input = int(user_input)
                if user_input <= 0:
                    raise ValueError("必须大于0")
            elif input_type == bool:
                user_input = user_input.lower()
                if user_input in ['y', 'yes', '是']:
                    return True
                elif user_input in ['n', 'no', '否']:
                    return False
                raise ValueError
            
            # 检查选项是否有效
            if valid_options and user_input not in valid_options:
                raise ValueError(f"请输入有效的选项: {', '.join(valid_options)}")
            
            return user_input
        
        except ValueError as e:
            print(f"输入无效: {e}")

def check_eligibility(attendee):
    """检查入场资格"""
    ticket_type = attendee['ticket_type']
    
    if ticket_type == 'VIP':
        return attendee['is_member']
    
    if ticket_type == '普通票':
        return attendee['age'] >= CONFIG['min_age']['普通票']
    
    if ticket_type == '学生票':
        return (attendee['age'] >= CONFIG['min_age']['学生票'] 
                and attendee['has_student_id'])
    
    return False

def add_attendee():
    """添加新的参与者"""
    clear_screen()
    show_header()
    print("【添加新参与者】\n")
    
    # 收集基本信息
    name = get_valid_input("姓名: ")
    age = get_valid_input("年龄: ", int)
    ticket_type = get_valid_input(
        f"票种({'/'.join(CONFIG['allowed_tickets'])}): ",
        valid_options=CONFIG['allowed_tickets']
    )
    
    # 根据票种收集额外信息
    is_member = False
    has_student_id = False
    
    if ticket_type == 'VIP':
        is_member = get_valid_input("是否是会员(Y/N): ", bool)
    elif ticket_type == '学生票':
        has_student_id = get_valid_input("是否有学生证(Y/N): ", bool)
    
    # 创建参与者记录
    new_attendee = {
        'name': name,
        'age': age,
        'ticket_type': ticket_type,
        'is_member': is_member,
        'has_student_id': has_student_id,
        'eligible': False  # 初始状态
    }
    
    # 检查资格
    new_attendee['eligible'] = check_eligibility(new_attendee)
    
    return new_attendee

def show_attendees(attendees):
    """显示参与者列表"""
    clear_screen()
    show_header()
    print("【参与者列表】\n")
    
    if not attendees:
        print("暂无参与者记录")
        return
    
    # 统计信息
    total = len(attendees)
    eligible = sum(1 for a in attendees if a['eligible'])
    
    print(f"总记录: {total} 条 | 符合条件: {eligible} 人\n")
    print("-"*70)
    print(f"{'姓名':<10}{'年龄':<6}{'票种':<8}{'会员':<6}{'学生证':<8}{'状态':<8}")
    print("-"*70)
    
    for attendee in attendees:
        print(
            f"{attendee['name']:<10}"
            f"{attendee['age']:<6}"
            f"{attendee['ticket_type']:<8}"
            f"{'是' if attendee['is_member'] else '否':<6}"
            f"{'是' if attendee.get('has_student_id', False) else '否':<8}"
            f"{'合格' if attendee['eligible'] else '不合格':<8}"
        )
    
    print("-"*70)

def main_menu():
    """主菜单"""
    attendees = load_data()
    
    while True:
        clear_screen()
        show_header()
        print("主菜单\n")
        print("1. 添加新参与者")
        print("2. 查看参与者列表")
        print("3. 保存并退出")
        print("4. 退出不保存\n")
        
        choice = get_valid_input("请选择操作(1-4): ", valid_options=['1','2','3','4'])
        
        if choice == '1':
            new_attendee = add_attendee()
            attendees.append(new_attendee)
            
            print("\n" + "="*50)
            if new_attendee['eligible']:
                print(f"【审核结果】{new_attendee['name']} 符合入场资格！")
            else:
                print(f"【审核结果】{new_attendee['name']} 不符合入场条件")
            print("="*50)
            
            input("\n按回车键返回主菜单...")
        
        elif choice == '2':
            show_attendees(attendees)
            input("\n按回车键返回主菜单...")
        
        elif choice == '3':
            save_data(attendees)
            print("\n数据已保存！")
            break
        
        elif choice == '4':
            print("\n退出系统，未保存更改！")
            break

if __name__ == '__main__':
    main_menu()
