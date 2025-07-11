from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# 职场16型人格数据
personality_types = {
    'GHzc': {
        'name': '纯粹实干家',
        'description': '专注价值创造，远离是非混乱。你是团队基石，可靠、高效、产出稳定。',
        'traits': ['目标导向', '执行力强', '避免冲突', '工作稳定'],
        'advice': '你是理想的团队成员，建议在保持现有优势的同时，可以适当提升影响力和创新思维。'
    },
    'GHZc': {
        'name': '实干谋略家',
        'description': '能力全面，懂规则。干活为主，整事能力用于自保或推动目标，稳定不整活。',
        'traits': ['能力全面', '政治敏感', '执行力强', '结果导向'],
        'advice': '你是核心贡献者和潜在领导者，需警惕"手腕"过度，保持正面影响力。'
    },
    'GhZc': {
        'name': '空想指挥官',
        'description': '干为主，懈于执行，不整事，稳定不整活。只规划不落地。',
        'traits': ['规划能力强', '执行力弱', '理想主义', '缺乏实践'],
        'advice': '你需要绑定强力执行者，或者加强自己的执行落地能力。'
    },
    'GHZC': {
        'name': '枭雄多面手',
        'description': '能力强贡献大，但也热衷权术且易制造混乱。关键角色但高风险。',
        'traits': ['能力突出', '政治手腕', '影响力强', '不稳定因素'],
        'advice': '你是高价值但高风险的角色，需要严格自我管理，将能力用于正面建设。'
    },
    'GhZC': {
        'name': '权谋战略家',
        'description': '善谋略搞政治，执行差、爱添乱。可能牺牲团队利益的潜在破坏者。',
        'traits': ['政治敏感', '战略思维', '执行力差', '制造混乱'],
        'advice': '建议将重心转向实际贡献，减少政治活动，提升执行能力。'
    },
    'GHzC': {
        'name': '进取探索者',
        'description': '有想法能执行，但方向/执行易偏带来小混乱。创新先锋但需要引导。',
        'traits': ['创新思维', '执行能力', '方向不稳', '偶尔混乱'],
        'advice': '你是创新驱动者，需要更好的方向把控和细节管理。'
    },
    'ghzc': {
        'name': '职场隐身人',
        'description': '存在感低，被动佛系。随、懈、和、稳，贡献微弱。',
        'traits': ['低调被动', '执行力弱', '避免冲突', '稳定保守'],
        'advice': '需要激活主动性，提升参与度和执行能力，发挥更大价值。'
    },
    'gHzc': {
        'name': '专注执行者',
        'description': '缺乏主动规划，但执行力强，不整事，稳定不整活。指哪打哪的可靠执行者。',
        'traits': ['执行力强', '服从性高', '缺乏主动性', '工作稳定'],
        'advice': '你是稳定基石，在明确任务下表现优秀，可以尝试提升主动规划能力。'
    },
    'gHZc': {
        'name': '腹黑老黄牛',
        'description': '执行力好但搞政治、易出错。沉默的火山，需要关注的矛盾体。',
        'traits': ['执行能力', '政治手腕', '情绪隐藏', '偶尔出错'],
        'advice': '你贡献稳定但有隐患，建议将政治能力转为正面影响力。'
    },
    'ghZc': {
        'name': '勤恳笨手',
        'description': '努力但能力差/粗心，常出错。态度好产出差，需要培训或调岗。',
        'traits': ['态度积极', '能力不足', '经常出错', '需要指导'],
        'advice': '你的态度值得肯定，建议加强专业技能培训，提升工作质量。'
    },
    'ghZC': {
        'name': '纠结麻烦精',
        'description': '能力差、产出糟，还搞小动作，负能量源。效率低、质量差、影响氛围。',
        'traits': ['能力不足', '制造麻烦', '负面影响', '效率低下'],
        'advice': '需要根本性改变，重新评估职业方向，或者寻求全面提升。'
    },
    'GhzC': {
        'name': '不羁梦想家',
        'description': '有想法但执行差，不整事，制造混乱。方向偏、执行烂的高风险实验者。',
        'traits': ['创意思维', '执行力差', '方向不明', '制造混乱'],
        'advice': '需要严格约束和指导，将创意转化为实际价值。'
    },
    'ghzC': {
        'name': '天真小白',
        'description': '能力差专注低，稳定制造混乱，人畜无害但持续出错需善后。',
        'traits': ['天真无害', '能力不足', '专注力差', '经常出错'],
        'advice': '需要系统培训或考虑转岗，提升基础能力和专注度。'
    },
    'gHZC': {
        'name': '灾难制造机',
        'description': '搞政治+能力差/爱添乱，破坏力极强的超级毒瘤。',
        'traits': ['破坏力强', '政治活跃', '能力不足', '制造混乱'],
        'advice': '需要立即处理和改变，重新评估职业适应性。'
    },
    'GHcz': {
        'name': '理想主义者',
        'description': '推动目标、高效执行、促进和谐。力求完美合作的团队粘合剂。',
        'traits': ['完美主义', '执行力强', '促进合作', '价值驱动'],
        'advice': '你是珍稀的理想员工，继续发挥价值的同时注意避免过度完美主义。'
    },
    'Ghzc': {
        'name': '务实守护者',
        'description': '干活为主，不整事，稳定不整活。更侧重守护和执行既定目标的稳定基石。',
        'traits': ['务实稳定', '执行导向', '避免风险', '守护价值'],
        'advice': '你是团队中流砥柱，可以在保持稳定的基础上适当增强主动性。'
    }
}

# 测试题目
questions = [
    {
        'id': 1,
        'question': '面对一个模糊的新项目时，你更倾向于：',
        'options': [
            {'text': '立刻梳理目标、拆解步骤，主动召集大家讨论', 'weight': {'G': 2}},
            {'text': '等领导明确具体要求后再动手', 'weight': {'g': 2}},
            {'text': '先观察谁负责、谁有资源，盘算如何参与对自己有利', 'weight': {'Z': 2}},
            {'text': '按自己理解先搞个炫酷的Demo，细节以后再说', 'weight': {'C': 2}}
        ]
    },
    {
        'id': 2,
        'question': '当接到一个枯燥但重要的重复性任务时，你通常会：',
        'options': [
            {'text': '制定高效流程，保质保量快速完成，甚至优化它', 'weight': {'H': 2}},
            {'text': '按部就班做完，不求快但求别出错', 'weight': {'h': 2}},
            {'text': '想办法推给别人，或拉更多人"分担"', 'weight': {'Z': 2}},
            {'text': '加点"创意"让它有趣点，哪怕可能偏离要求', 'weight': {'C': 2}}
        ]
    },
    {
        'id': 3,
        'question': '发现同事的方案有明显漏洞时，你会：',
        'options': [
            {'text': '直接指出问题并提出改进建议', 'weight': {'G': 2}},
            {'text': '默默做好自己部分，别人的问题不插手', 'weight': {'z': 2}},
            {'text': '私下告诉领导/关键人物，凸显自己价值', 'weight': {'Z': 2}},
            {'text': '按照错误方案执行，等出问题了再说', 'weight': {'h': 1, 'C': 1}}
        ]
    },
    {
        'id': 4,
        'question': '团队会议上讨论陷入僵局，你的角色常是：',
        'options': [
            {'text': '提出新框架或折中方案推动决策', 'weight': {'G': 2}},
            {'text': '听从最后拍板的人，让干啥就干啥', 'weight': {'g': 1, 'z': 1}},
            {'text': '暗中支持对自己有利的一方，或搅浑水', 'weight': {'Z': 2}},
            {'text': '抛出天马行空的想法转移焦点，不管是否可行', 'weight': {'C': 2}}
        ]
    },
    {
        'id': 5,
        'question': '工作出现失误导致延误，你的第一反应是：',
        'options': [
            {'text': '分析原因、制定补救计划，主动汇报', 'weight': {'G': 1, 'H': 1}},
            {'text': '非常焦虑，等别人发现或询问再解释', 'weight': {'h': 2}},
            {'text': '找客观原因或暗示是他人/协作方的责任', 'weight': {'Z': 2}},
            {'text': '用幽默/创意方式掩饰，希望蒙混过关', 'weight': {'C': 2}}
        ]
    },
    {
        'id': 6,
        'question': '如何对待工作流程和文档？',
        'options': [
            {'text': '严格遵守并优化，确保可追溯性', 'weight': {'H': 2}},
            {'text': '按最低要求完成，不出错就行', 'weight': {'h': 2}},
            {'text': '利用流程漏洞为自己争取便利或设置门槛', 'weight': {'Z': 2}},
            {'text': '觉得太繁琐常跳过，结果漏步骤或信息不全', 'weight': {'C': 2}}
        ]
    },
    {
        'id': 7,
        'question': '获得额外资源（预算/人力/权限）时，你优先用于：',
        'options': [
            {'text': '攻克关键瓶颈或尝试战略创新', 'weight': {'G': 2}},
            {'text': '减轻现有工作压力，求稳', 'weight': {'g': 2}},
            {'text': '巩固自己地位，拉拢盟友或排挤对手', 'weight': {'Z': 2}},
            {'text': '试验感兴趣但可能不相关的"黑科技"', 'weight': {'C': 2}}
        ]
    },
    {
        'id': 8,
        'question': '如何看待跨部门合作？',
        'options': [
            {'text': '主动对齐目标，推动高效协作', 'weight': {'G': 1, 'z': 1}},
            {'text': '对方找我就配合，不找我不主动', 'weight': {'g': 1, 'h': 1}},
            {'text': '视为争夺影响力和资源的机会', 'weight': {'Z': 2}},
            {'text': '常因沟通不畅或理解偏差引发误会', 'weight': {'C': 2}}
        ]
    },
    {
        'id': 9,
        'question': '领导布置一个超高难度任务时，你更可能：',
        'options': [
            {'text': '评估可行性后，挑战并制定攻坚计划', 'weight': {'G': 2}},
            {'text': '感到压力山大，硬着头皮尽力做', 'weight': {'h': 2}},
            {'text': '强调困难争取更多资源支持，或甩给"能者"', 'weight': {'Z': 2}},
            {'text': '兴奋尝试新方法，但可能忽略基础工作', 'weight': {'C': 2}}
        ]
    },
    {
        'id': 10,
        'question': '你最大的职场成就感来自：',
        'options': [
            {'text': '推动重要项目成功落地', 'weight': {'G': 2}},
            {'text': '工作零差错，获得稳定信任', 'weight': {'H': 2}},
            {'text': '在博弈中获胜，获得权力/影响力', 'weight': {'Z': 2}},
            {'text': '做出让人眼前一亮的"神操作"', 'weight': {'C': 2}}
        ]
    }
]

def calculate_personality_type(answers):
    """根据答案计算人格类型"""
    scores = {'G': 0, 'g': 0, 'H': 0, 'h': 0, 'Z': 0, 'z': 0, 'C': 0, 'c': 0}
    
    for i, answer in enumerate(answers):
        if i < len(questions) and answer < len(questions[i]['options']):
            weights = questions[i]['options'][answer]['weight']
            for dimension, weight in weights.items():
                scores[dimension] += weight
    
    # 确定每个维度的显性或隐性
    result = ''
    
    # G维度判断
    if scores['G'] >= scores['g']:
        result += 'G'
    else:
        result += 'g'
    
    # H维度判断
    if scores['H'] >= scores['h']:
        result += 'H'
    else:
        result += 'h'
    
    # Z维度判断
    if scores['Z'] >= scores['z']:
        result += 'Z'
    else:
        result += 'z'
    
    # C维度判断
    if scores['C'] >= scores['c']:
        result += 'C'
    else:
        result += 'c'
    
    return result

@app.route('/test-simple')
def test_simple():
    return "<h1>Flask应用正在运行！</h1><p>如果你看到这个页面，说明Flask正常工作。</p>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit_test():
    answers = request.json.get('answers', [])
    
    if len(answers) != 10:
        return jsonify({'error': '请完成所有题目'}), 400
    
    personality_type = calculate_personality_type(answers)
    result = personality_types.get(personality_type, {
        'name': '未知类型',
        'description': '抱歉，无法确定您的职场人格类型。',
        'traits': [],
        'advice': '建议重新进行测试。'
    })
    
    return jsonify({
        'type': personality_type,
        'result': result
    })

if __name__ == '__main__':
    # 允许局域网访问
    app.run(debug=True, host='0.0.0.0', port=5000)
