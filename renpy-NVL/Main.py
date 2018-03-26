# Python 3.x support only
# Author: BlueM1ST
# Version: 0.2
# Purpose: help convert ren'py games to NVLMaker Cloud
# Method: replace ren'py tags and variables with similar NVLMaker Cloud tags and variables
# Limitations: cannot convert anything made with pygame

import re

class Main:

    def printToFile(self):
        selection = False
        ren = open("test.txt", "r")
        nvl = open("out.txt", "w")
        renLines = ren.readlines()

        for line in renLines:

            if not(selection):

                if('label' in line):
                    line = line.replace('label ', '*').replace(':' or ' :', '')
                    print(line)
                    nvl.writelines(line)

                elif ('#' in line and not 'define' in line):
                    line = line.replace('#', '//')
                    print(line)
                    nvl.writelines(line)

                elif('scene' in line):
                    line = line.replace('bg ', '').replace('scene ', '@bg storage=f.')\
                        .replace('with dissolve', 'method="crossfade"')
                    line = re.sub(r"=\w+\s\w+", lambda x: x.group(0).replace(' ', '_'), line)
                    print(line)
                    nvl.writelines(line)

                elif('show' in line and not '"' in line and not 'show text' in line):
                    line = line.replace('show ', '@fgin storage=f.')\
                        .replace('with dissolve', 'method="crossfade"') \
                        .replace('with moveinleft', 'from="l"') \
                        .replace('with moveinright', 'from="r"') \
                        .replace('at left', 'pos="left"') \
                        .replace('at right', 'pos="right"')\
                        .replace('at center', 'pos="center"')
                    line = re.sub(r"=f.\w+\s\w+", lambda x: x.group(0).replace(' ', '_'), line)
                    print(line)
                    nvl.writelines(line)

                # comment out the show text, not sure how to deal with them
                elif('show text' in line):
                    line = line.replace('    ', '')
                    line = "//" + line
                    print(line)
                    nvl.writelines(line)

                elif('play sound' in line):
                    line = line.replace('play sound ', '@se storage=').replace('loop', 'loop="true"') \
                        .replace('    ', '')
                    print(line)
                    nvl.writelines(line)

                # comment out the pauses, =not sure how to deal with them=
                elif('pause' in line and not '"' in line):
                    line = line.replace('    ', '')
                    line = "//" + line
                    print(line)
                    nvl.writelines(line)

                elif('play music' in line):
                    line = line.replace('play music ', '@bgm storage=').replace('loop', 'loop="true"') \
                        .replace('    ', '')
                    if('fadein' in line or 'fadeout' in line):
                        line = line.replace('fadeout ', 'time="').replace('fadein ', 'time="').replace('\n', '')
                        line = line + '"\n'
                        print(line)
                        nvl.writelines(line)
                    else:
                        print(line)
                        nvl.writelines(line)

                # for variables
                elif ('$' in line or 'default' in line or 'define' in line or 'image' in line):
                        line = line.replace('$ ', 'var').replace('default ', 'var').replace('define ', 'var')\
                            .replace('\n', '').replace('    ', '').replace('True', 'true').replace('image ', 'var')

                        # add an underline to variable anmes that have two words (variables should all be one word)
                        line = re.sub(r"\w+\s\w+", lambda x:x.group(0).replace(' ','_'), line)
                        line = line.replace('bg_', ' ').replace('var ', 'f.').replace('var', 'f.')

                        #only can set to string, not tag
                        if ('Character' in line):
                            line = line.replace('Character (', '').replace('Character(', '')
                            line = line.replace(line.split(',', 1)[1], '').replace(',', '')
                            line = '#' + line + ';\n'
                            print(line)
                            nvl.writelines(line)

                        elif('renpy.' in line):
                            line = line.replace('    ', '')
                            line = "//" + line
                            print(line)
                            nvl.writelines(line)

                        else:
                            line = '#' + line + ';\n'
                            print(line)
                            nvl.writelines(line)

                # for text
                elif ('"' in line
                      and not '$' in line
                      and not 'play' in line
                      and not 'image' in line
                      and not '#' in line
                      and not 'define' in line):
                    # if there is a character name on screen
                    if (re.match(r'(\s\s\s\s\w+\s+")', line) or re.match(r'(\s\s\s\s\s\w+\s+")', line) or '"[name]"' in line):
                        line = 'npc id=f.' + line.replace('     ', '').replace('    ', '').replace('"[name]"', 'name')\
                            .replace('[name]', 'name')
                        line = line.replace('\n', '') + '[w]\n'
                        # add brackets around the @npc tag
                        linex = line.split(' "', 1)[0]
                        line = line.replace(line.split('"', 1)[0], '[' + linex + ']\n')

                        # if nonexisting syling tags
                        if ('b}' in line or 'i}' in line or 's}'):
                            line = line.replace('{b}', '').replace('{/b}', '') \
                                .replace('{i}', '').replace('{/i}', '') \
                                .replace('{s}', '').replace('{/s}', '')
                            print(line)
                            nvl.writelines(line)

                        else:
                            print(line)
                            nvl.writelines(line)

                    # if there is no character name on screen
                    else:
                        line = line.replace('\n', '').replace('[name]', 'name') + '[w]\n'

                        # if nonexisting syling tags
                        if ('b}' in line or 'i}' in line or 's}'):
                            line = line.replace('{b}', '').replace('{/b}', '') \
                                .replace('{i}', '').replace('{/i}', '') \
                                .replace('{s}', '').replace('{/s}', '')
                            print(line)
                            nvl.writelines(line)

                        else:
                            print(line)
                            nvl.writelines(line)

                elif('menu:' in line or 'menu :' in line):
                    line = line.replace('menu:', '@selstart').replace('menu :', '@selstart')
                    selection = True
                    print(line)
                    nvl.writelines(line)

                else:
                    print('passed')
                    nvl.writelines('\n')
                    pass

            # if in a selection menu =================================================
            else:
                if(':' in line and not '$' in line and not 'label' in line):
                    line = '@selbutton text=' + line
                    line = line.replace('\n', '').replace(':', '').replace('     ', '').replace('    ', '')
                    print(line)
                    nvl.writelines(line)

                elif('jump' in line):
                    line = line.replace('\n', '').replace(' jump ', '').replace('      ', '').replace('    ', '')
                    line = 'target=' + '"*' + line + '"\n'
                    print(line)
                    nvl.writelines(line)

                # if the label is in the select block, everything breaks
                elif('label' in line):
                    line = '@selend\n\n' + line.replace('label ', '*').replace(':' or ' :', '')
                    print(line)
                    nvl.writelines(line)
                    selection = False

                else:
                    print('passed')
                    nvl.writelines('')
                    pass

        ren.close()
        nvl.close()


mainClass = Main()


def main():
    print('==Begin conversion==')
    mainClass.printToFile()

main()
