import pygame
import sys
import random
import collections
from agent import Agent_wsct
import csv


SCREEN_X = 1200
SCREEN_Y = 800

Num = ['1','2','3','4']
Color = ['red','green','blue','yellow']
Shape = ['circle','square','triangle','star']
RULE_DICT = {"shape":2,"color":1,"num":0,"None":3}
ACTION_SET = {0:(460,475),1:(640,475),2:(820,475),3:(1000,475)}
f = open("sample.txt","w")

class Card(object):
    def __init__(self,num,color,shape):
        self.num = num
        self.color = color
        self.shape = shape
        self.state = [Num.index(num),Color.index(color),Shape.index(shape)]
        self.image = pygame.image.load("img/"+shape+color+num+".png")
        self.rect = self.image.get_rect()
        action = [0,0,0]
        
class game(object):
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
        self.screen.fill((0,0,0))
        # self.actions = {"choose1":[1,0,0,0],"choose2":[0,1,0,0],"choose3":[0,0,1,0],"choose4":[0,0,0,1]}
        pygame.display.set_caption('WCST')
        self.choose = None
        self.result = 3
        self.NOOP = pygame.K_F13
        self.last_action = []
        #设置4张底牌，随机变化
        self.Card1 = Card(Num[0],Color[0],Shape[0])
        self.Card2 = Card(Num[1],Color[1],Shape[1])
        self.Card3 = Card(Num[2],Color[2],Shape[2])
        self.Card4 = Card(Num[3],Color[3],Shape[3])
        #得到鼠标位置
        self.mouse_x = 0
        self.mouse_y = 0
        self.rules = ['num','color','shape']
        #法官牌
        self.Stim = Card(Num[random.randint(0,3)],Color[random.randint(0,3)],Shape[random.randint(0,3)])
        self.font = pygame.font.SysFont('SimHei',30)
        self.instruction = self.font.render("Choose one of the four cards match the card on the left", 1, (255, 255, 255))
        self.rect1 = pygame.Rect(500,160,100,80)
        self.rect2 = pygame.Rect(680,160,100,80)
        self.rect3 = pygame.Rect(860,160,100,80)
        pygame.draw.rect(self.screen,(255,255,255),self.rect1)
        pygame.draw.rect(self.screen,(255,255,255),self.rect2)
        pygame.draw.rect(self.screen,(255,255,255),self.rect3)
        choose_color = self.font.render("COLOR",True,(0,0,0))
        choose_num = self.font.render("NUMBER",True,(0,0,0))
        choose_shape = self.font.render("SHAPE",True,(0,0,0))
        color_rect = choose_color.get_rect()
        num_rect = choose_num.get_rect()
        shape_rect = choose_shape.get_rect()
        color_rect.midtop = (550,185)
        num_rect.midtop = (730,185)
        shape_rect.midtop = (910,185)
        self.screen.blit(choose_color, color_rect)
        self.screen.blit(choose_num, num_rect)
        self.screen.blit(choose_shape, shape_rect)
        pygame.display.flip()
        self.correct_img = pygame.image.load("img/correct.png")
        self.wrong_img = pygame.image.load("img/wrong.png")
        self.cover_img = pygame.image.load("img/cover.png")
        self.screen.blit(self.Card1.image,(400,400))
        self.screen.blit(self.Card2.image,(580,400))
        self.screen.blit(self.Card3.image,(760,400))
        self.screen.blit(self.Card4.image,(940,400))
        self.screen.blit(self.Stim.image,(150,200))
        self.screen.blit(self.instruction,(300,100))
        self.flag = 0
        self.per_flag = 0
        self.Correct = 0
        self.Wrong = 0
        self.per_error = 0
        self.per_response = 0
        self.Trial = 0
        self.n = 10
        self.rule = self.rules[random.randint(0,2)]
        self.last_rule = None

    def act(self,action):
        if action is not None:
            self._setAction(action,self.last_action)
        else:
            self.step(action)
        self.last_action = action

    def _setAction(self, action, last_action):
        if 1 not in action or action is None:
            action = self.NOOP

        if 1 not in last_action or last_action is None:
            last_action = self.NOOP

        if action !=self.NOOP and last_action!=self.NOOP:
            kd = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": ACTION_SET[action.index(1)],"button":1})
            pygame.event.post(kd)
        else:
            kd = pygame.event.Event(pygame.KEYDOWN,{"key":action})
            ku = pygame.event.Event(pygame.KEYDOWN,{"key":last_action})
            pygame.event.post(kd)
            pygame.event.post(ku)

    def _handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    f.close()
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.result = 0
                if event.pos[0] <= 520 and event.pos[0] >= 400 and event.pos[1] <= 550 and event.pos[1] >= 400:
                    self.flag = 1
                    self.n += -1
                    if self.rule == 'num':
                        if self.Stim.num == self.Card1.num:
                            self.screen.blit(self.correct_img, (400, 250))
                            self.Correct += 1
                            self.Trial += 1
                            self.result = 1
                        else:
                            self.screen.blit(self.wrong_img, (400, 250))
                            self.Wrong += 1
                            self.Trial += 1
                            if self.per_flag:
                                if self.last_rule == 'color':
                                    if self.Stim.color == self.Card1.color:
                                        self.per_error += 1
                                else:
                                    if self.Stim.shape == self.Card1.shape:
                                        self.per_error += 1
                    elif self.rule == 'color':
                        if self.Stim.color == self.Card1.color:
                            self.screen.blit(self.correct_img, (400, 250))
                            self.Correct += 1
                            self.result = 1
                            self.Trial += 1
                        else:
                            self.screen.blit(self.wrong_img, (400, 250))
                            self.Wrong += 1
                            self.Trial += 1
                            if self.per_flag:
                                if self.last_rule == 'num':
                                    if self.Stim.num == self.Card1.num:
                                        self.per_error += 1
                                else:
                                    if self.Stim.shape == self.Card1.shape:
                                        self.per_error += 1
                    else:
                        if self.Stim.shape == self.Card1.shape:
                            self.screen.blit(self.correct_img, (400, 250))
                            self.Correct += 1
                            self.result = 1
                            self.Trial += 1
                        else:
                            self.screen.blit(self.wrong_img, (400, 250))
                            self.Wrong += 1
                            self.Trial += 1
                            if self.per_flag:
                                if self.last_rule == 'color':
                                    if self.Stim.color == self.Card1.color:
                                        self.per_error += 1
                                else:
                                    if self.Stim.num == self.Card1.num:
                                        self.per_error += 1
                    self.Stim = Card(Num[random.randint(0, 3)], Color[random.randint(0, 3)],
                                     Shape[random.randint(0, 3)])
                    self.screen.blit(self.Stim.image, (150, 200))
                    f.write(str((self.choose, self.result))+"\n")
                elif event.pos[0] <= 700 and event.pos[0] >= 580 and event.pos[1] <= 550 and event.pos[1] >= 400:
                    self.flag = 1
                    self.n += -1
                    if self.rule == 'num':
                        if self.Stim.num == self.Card2.num:
                            self.screen.blit(self.correct_img, (580, 250))
                            self.Correct += 1
                            self.result = 1
                            self.Trial += 1
                        else:
                            self.screen.blit(self.wrong_img, (580, 250))
                            self.Wrong += 1
                            self.Trial += 1
                            if self.per_flag:
                                if self.last_rule == 'color':
                                    if self.Stim.color == self.Card2.color:
                                        self.per_error += 1
                                else:
                                    if self.Stim.shape == self.Card2.shape:
                                        self.per_error += 1
                    elif self.rule == 'color':
                        if self.Stim.color == self.Card2.color:
                            self.screen.blit(self.correct_img, (580, 250))
                            self.Correct += 1
                            self.result = 1
                            self.Trial += 1
                        else:
                            self.screen.blit(self.wrong_img, (580, 250))
                            self.Wrong += 1
                            self.Trial += 1
                            if self.per_flag:
                                if self.last_rule == 'num':
                                    if self.Stim.num == self.Card2.num:
                                        self.per_error += 1
                                else:
                                    if self.Stim.shape == self.Card2.shape:
                                        self.per_error += 1
                    else:
                        if self.Stim.shape == self.Card2.shape:
                            self.screen.blit(self.correct_img, (580, 250))
                            self.Correct += 1
                            self.result = 1
                            self.Trial += 1
                        else:
                            self.screen.blit(self.wrong_img, (580, 250))
                            self.Wrong += 1
                            self.Trial += 1
                            if self.per_flag:
                                if self.last_rule == 'color':
                                    if self.Stim.color == self.Card2.color:
                                        self.per_error += 1
                                else:
                                    if self.Stim.num == self.Card2.num:
                                        self.per_error += 1
                    self.Stim = Card(Num[random.randint(0, 3)], Color[random.randint(0, 3)],
                                     Shape[random.randint(0, 3)])
                    self.screen.blit(self.Stim.image, (150, 200))
                    f.write(str((self.choose, self.result))+"\n")
                elif event.pos[0] <= 880 and event.pos[0] >= 760 and event.pos[1] <= 550 and event.pos[1] >= 400:
                    self.flag = 1
                    self.n += -1
                    if self.rule == 'num':
                        if self.Stim.num == self.Card3.num:
                            self.screen.blit(self.correct_img, (760, 250))
                            self.Correct += 1
                            self.result = 1
                            self.Trial += 1
                        else:
                            self.screen.blit(self.wrong_img, (760, 250))
                            self.Wrong += 1
                            self.Trial += 1
                            if self.per_flag:
                                if self.last_rule == 'color':
                                    if self.Stim.color == self.Card3.color:
                                        self.per_error += 1
                                else:
                                    if self.Stim.shape == self.Card3.shape:
                                        self.per_error += 1
                    elif self.rule == 'color':
                        if self.Stim.color == self.Card3.color:
                            self.screen.blit(self.correct_img, (760, 250))
                            self.result = 1
                            self.Correct += 1
                            self.Trial += 1
                        else:
                            self.screen.blit(self.wrong_img, (760, 250))
                            self.Wrong += 1
                            self.Trial += 1
                            if self.per_flag:
                                if self.last_rule == 'num':
                                    if self.Stim.num == self.Card3.num:
                                        self.per_error += 1
                                else:
                                    if self.Stim.shape == self.Card3.shape:
                                        self.per_error += 1
                    else:
                        if self.Stim.shape == self.Card3.shape:
                            self.screen.blit(self.correct_img, (760, 250))
                            self.Correct += 1
                            self.result = 1
                            self.Trial += 1
                        else:
                            self.screen.blit(self.wrong_img, (760, 250))
                            self.Wrong += 1
                            self.Trial += 1
                            if self.per_flag:
                                if self.last_rule == 'color':
                                    if self.Stim.color == self.Card3.color:
                                        self.per_error += 1
                                else:
                                    if self.Stim.num == self.Card3.num:
                                        self.per_error += 1
                    self.Stim = Card(Num[random.randint(0, 3)], Color[random.randint(0, 3)],
                                     Shape[random.randint(0, 3)])
                    self.screen.blit(self.Stim.image, (150, 200))
                    f.write(str((self.choose, self.result))+"\n")
                elif event.pos[0] <= 1060 and event.pos[0] >= 940 and event.pos[1] <= 550 and event.pos[1] >= 400:
                    self.flag = 1
                    self.n += -1
                    if self.rule == 'num':
                        if self.Stim.num == self.Card4.num:
                            self.screen.blit(self.correct_img, (940, 250))
                            self.Correct += 1
                            self.result = 1
                            self.Trial += 1
                        else:
                            self.screen.blit(self.wrong_img, (940, 250))
                            self.Wrong += 1
                            self.Trial += 1
                            if self.per_flag:
                                if self.last_rule == 'color':
                                    if self.Stim.color == self.Card4.color:
                                        self.per_error += 1
                                else:
                                    if self.Stim.shape == self.Card4.shape:
                                        self.per_error += 1
                    elif self.rule == 'color':
                        if self.Stim.color == self.Card4.color:
                            self.screen.blit(self.correct_img, (940, 250))
                            self.Correct += 1
                            self.result = 1
                            self.Trial += 1
                        else:
                            self.screen.blit(self.wrong_img, (940, 250))
                            self.Wrong += 1
                            self.Trial += 1
                            if self.per_flag:
                                if self.last_rule == 'num':
                                    if self.Stim.num == self.Card4.num:
                                        self.per_error += 1
                                else:
                                    if self.Stim.shape == self.Card4.shape:
                                        self.per_error += 1
                    else:
                        if self.Stim.shape == self.Card4.shape:
                            self.screen.blit(self.correct_img, (940, 250))
                            self.Correct += 1
                            self.result = 1
                            self.Trial += 1
                        else:
                            self.screen.blit(self.wrong_img, (940, 250))
                            self.Wrong += 1
                            self.Trial += 1
                            if self.per_flag:
                                if self.last_rule == 'color':
                                    if self.Stim.color == self.Card4.color:
                                        self.per_error += 1
                                else:
                                    if self.Stim.num == self.Card4.num:
                                        self.per_error += 1
                    self.Stim = Card(Num[random.randint(0, 3)], Color[random.randint(0, 3)],
                                     Shape[random.randint(0, 3)])
                    self.screen.blit(self.Stim.image, (150, 200))
                    f.write(str((self.choose, self.result))+"\n")
                elif event.pos[0] <= 600 and event.pos[0] >= 500 and event.pos[1] <= 240 and event.pos[1] >= 160:
                    self.choose = "COLOR"
                elif event.pos[0] <= 780 and event.pos[0] >= 680 and event.pos[1] <= 240 and event.pos[1] >= 160:
                    self.choose = "NUMBER"
                elif event.pos[0] <= 960 and event.pos[0] >= 860 and event.pos[1] <= 240 and event.pos[1] >= 160:
                    self.choose = "SHAPE"
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                # print(pos)
                self.mouse_x = pos[0]
                self.mouse_y = pos[1]

    def getState(self):
        import copy
        platform_state = list()
        card1_state = copy.deepcopy(self.Card1.state)
        card1_state.insert(0,1) 
        card2_state = copy.deepcopy(self.Card2.state)
        card2_state.insert(0,2)
        card3_state = copy.deepcopy(self.Card3.state)
        card3_state.insert(0,3)
        card4_state = copy.deepcopy(self.Card4.state)
        card4_state.insert(0,4)
        cardstim_state = copy.deepcopy(self.Stim.state)
        cardstim_state.insert(0,0)
        platform_state.extend(cardstim_state)
        platform_state.extend(card1_state)
        platform_state.extend(card2_state)
        platform_state.extend(card3_state)
        platform_state.extend(card4_state)
        return platform_state

    def reset(self):
        self.screen.fill((0,0,0))
        self.Stim = Card(Num[random.randint(0,3)],Color[random.randint(0,3)],Shape[random.randint(0,3)])
        self.last_action = []
        self.screen.blit(self.Card1.image,(400,400))
        self.screen.blit(self.Card2.image,(580,400))
        self.screen.blit(self.Card3.image,(760,400))
        self.screen.blit(self.Card4.image,(940,400))
        self.screen.blit(self.Stim.image,(150,200))
        self.screen.blit(self.instruction,(300,100))
        self.flag = 0
        self.per_flag = 0
        self.Correct = 0
        self.Wrong = 0
        self.per_response = 0
        self.per_corrects = 0
        self.per_error = 0
        self.Trial = 0
        self.n = 10
        self.rule = self.rules[random.randint(0,2)]
        self.last_rule = None
        pygame.display.update()
        return self.Stim.state

    # def step(self,action):
    #     tmp = self.rule
    #     if self.n == 0:
    #         self.per_flag = 1
    #         self.n = 10
    #         while (tmp==self.rule):
    #             self.last_rule = self.rule
    #             tmp = self.rules[random.randint(0,2)]
    #         self.rule = tmp
    #     if action.index(max(action)) == 0:
    #         self.Trial += 1
    #         self.n -= 1
    #         if self.rule == 'num':
    #             reward = 1
    #             self.Correct += 1
    #         else:
    #             reward = 0
    #             self.Wrong += 1
    #             if self.per_flag:
    #                 if self.last_rule == 'num':
    #                     self.per_error += 1
    #     elif action.index(max(action)) == 1:
    #         self.Trial += 1
    #         self.n -= 1
    #         if self.rule == 'color':
    #             reward = 1
    #             self.Correct += 1
    #         else:
    #             reward = 0
    #             self.Wrong += 1
    #             if self.per_flag:
    #                 if self.last_rule == 'color':
    #                     self.per_error += 1
    #     else:
    #         self.Trial += 1
    #         self.n -= 1
    #         if self.rule == 'shape':
    #             reward = 1
    #             self.Correct += 1
    #         else:
    #             reward = 0
    #             self.Wrong += 1
    #             if self.per_flag:
    #                 if self.last_rule == 'shape':
    #                     self.per_error += 1
    #     self.Stim = Card(Num[random.randint(0,3)],Color[random.randint(0,3)],Shape[random.randint(0,3)])
    #     return self.Stim.platform_state, reward, self.Trial>60, [self.Correct,self.Wrong,self.per_error]

    def run(self):
        tmp = self.rule
        if self.flag:
#             pygame.time.delay(500)
            self.screen.blit(self.cover_img,(400,250))
            self.screen.blit(self.cover_img,(760,250))
            self.screen.blit(self.cover_img,(580,250))
            self.screen.blit(self.cover_img,(940,250))
            self.flag = 0
        self._handle_event()
        if self.n == 0:
            self.per_flag = 1
            self.n = 10
            while (tmp==self.rule):
                self.last_rule = self.rule
                tmp = self.rules[random.randint(0,2)]
            self.rule = tmp
        
        pygame.display.flip()
#         pygame.time.delay(50)

    def show_results(self):
        self.screen.fill((0, 0, 0))
        textobj1 = self.font.render("Number of correctness: " + str(self.Correct), 1, (255, 255, 255))  # 正确应答数
        textobj2 = self.font.render("Number of errors: " + str(self.Wrong), 1, (255, 255, 255))  # 错误应答数
        textobj3 = self.font.render("Feedback on your WCST performance (in 60 trials)", 1, (255, 255, 255))
        textobj4 = self.font.render("Number of perseveration errors: " + str(self.per_error), 1, (255, 255, 255))
        textobj5 = self.font.render("Number of non-perseveration errors: " + str(self.Wrong - self.per_error), 1,
                                    (255, 255, 255)) 
        textobj6 = self.font.render("[" + str(format((self.per_error / 60)*100,"0.2f")) +"%" +"]", 1, (255, 255, 255))
        textobj7 = self.font.render("[" + str(format(((self.Wrong - self.per_error)/60)*100,"0.2f")) +"%" +"]", 1, (255, 255, 255))
        self.screen.blit(textobj1, (350, 200))
        self.screen.blit(textobj2, (350, 300))
        self.screen.blit(textobj3, (300, 100))
        self.screen.blit(textobj4, (350, 400))
        self.screen.blit(textobj5, (350, 500))
        self.screen.blit(textobj6, (900, 400))
        self.screen.blit(textobj7, (950, 500))
        pygame.display.update()
        pygame.time.delay(10000)

    def game_over(self):
        if self.Trial>=60:
            self.show_results()
            self.reset()
            return True
        else:
            return False

def Static_results():
    f_static_res = open('./results/term_static.csv','w',newline='')
    csv_write_res = csv.writer(f_static_res,dialect = 'excel')
    for i in range(20):
        g = game()
        agent = Agent_wsct()
        last_dec = 0
        decision_stack = collections.deque(maxlen=6)
    #     f_static = open('./results/term1.txt','w')
    #     f_static.write('plantform_state \t plantform_rule \t plantform_label \t agnet_decision \t agnent_action\n')
        f_static = open('./results/term_%d_detail.csv'%i,'w',newline='')
        csv_write = csv.writer(f_static,dialect = 'excel')
        print('plantform_state \t plantform_rule \t plantform_label \t agnet_decision \t agnent_action\n')
        csv_write.writerow(['plantform_state','plantform_rule','plantform_label','agnet_decision','agnent_action'])
        for i in range(2):
            decision_stack.append([0,0])
        while not g.game_over():
            g.run()
            platform_state = g.getState() #获得当前平台的态势(五张牌，每张牌由4个特征表示)
            last_round_result = g.result #获得上一轮做出decision后，选择的牌是否正确
    #         print(platform_state,last_round_result)
            platform_current_rule = RULE_DICT[g.rule] # 获得平台当前时刻的规则
            platform_current_card = g.Stim.state[RULE_DICT[g.rule]] # 获得平台当前应当选择哪一个卡牌
            
            decision_stack.append([last_dec,last_round_result])
            print('current decision_stack ',decision_stack) 
            action,decision= agent.run(situation=platform_state,previous_decision = decision_stack)
    #         f_static.write(res)
            csv_write.writerow([platform_state,platform_current_rule,platform_current_card,
                                                      decision[0], action[0]])
            # action为根据当前态势及策略选择的卡牌；decision为基于前N轮决策及决策的正确与否预测出这轮的策略
            last_dec = decision[0]
            action_set = [0,0,0,0]
            action_set [action[0]]= 1
            g.act(action_set)
        one_term_res = [g.Correct,g.Wrong,g.per_error,g.Wrong-g.per_error,g.per_error/60*100,(g.Wrong-g.per_error)/60*100]
        csv_write_res.writerow(one_term_res)
        f_static.close()
    f_static_res.close()



if __name__=="__main__":
    g = game()
    agent = Agent_wsct()
    step = 6
    decision_stack = collections.deque(maxlen=step)
    f_static = open('./results/V4_detail_step%d.csv'%step,'w',newline='')
    csv_write = csv.writer(f_static,dialect = 'excel')
    csv_write.writerow(['plantform_state','plantform_rule','plantform_label','agnet_decision','agnent_action'])
    for i in range(step):
        decision_stack.append([3,3])
    while not g.game_over():
        g.run()
        platform_state = g.getState() #获得当前平台的态势(五张牌，每张牌由4个特征表示)
        last_round_result = g.result #获得上一轮做出decision后，选择的牌是否正确
        platform_current_rule = RULE_DICT[g.rule] # 获得平台当前时刻的规则
        platform_current_card = g.Stim.state[RULE_DICT[g.rule]] # 获得平台当前应当选择哪一个卡牌
        
        action,decision= agent.run(situation=platform_state,previous_decision = decision_stack)
        csv_write.writerow([platform_state,platform_current_rule,platform_current_card,
                                                  decision[0], action[0]])
        # action为根据当前态势及策略选择的卡牌；decision为基于前N轮决策及决策的正确与否预测出这轮的策略
        last_dec = decision[0]
        action_set = [0,0,0,0]
        action_set [action[0]]= 1
        g.act(action_set)
        if decision[0] == platform_current_rule:
            decision_stack.append([decision[0],1])
        else:
            decision_stack.append([decision[0],0])
        print('end of term,decision stack is ',decision_stack)
    f_static.close()

