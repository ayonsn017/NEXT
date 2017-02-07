def get_pretest_instruction():
    """
    :return: string, the instruction for the pretest questions
    """

    return '<h2>In the following section we will show the images of two molecules. You have to judge if the two molecules are the same or not.</h2>'

def get_training_instruction():
    """
    :return: string, the instruction for the training questions
    """

    return '<h2>The next set of questions will now start.</h2>'

def get_posttest_instruction():
    """
    :return: string, the instruction for the posttest questions
    """

    return '<h2>The final set of questions will now start.</h2>'

def get_introduction_instruction1():
    """
    :return: string, the first introduction instruction
    """

    return """<h1>UNIVERSITY OF WISCONSIN-MADISON</h1>
<h1>Research Participant Information and Consent Form</h1><br>
<b>Title of the Study:</b> Chemistry representations test<br><br>
<b>Principal Investigator:</b> Martina Rau (phone: 608-262-0833) (email: marau@wisc.edu)<br><br>
<h2>DESCRIPTION OF THE RESEARCH</h2><br>
You are invited to take a study about visual learning in chemistry. You will answer questions about chemistry representations.<br>
You have been asked to participate because you are taking or have taken a chemistry course.<br>
The purpose of the research is to find out how you learn with visual representations.<br>
This study will include student volunteers, recruited from UW Madison.
The survey will be conducted online. The test is fully confidential and will not assess sensitive information.<br>
<h2>WHAT WILL MY PARTICIPATION INVOLVE?</h2><br>
If you decide to take this test, you will be asked to answer a set of up to 126 questions. The test will take about 10 minutes. <br>
<h2>ARE THERE ANY RISKS TO ME?</h2><br>
We don't anticipate any risks to you from participation in this study.<br>
<h2>ARE THERE ANY BENEFITS TO ME?</h2><br>
There are no direct guaranteed benefits in participating in this study.<br> 
<h2>WILL I BE COMPENSATED FOR MY PARTICIPATION?</h2><br>
You will be entered in a lottery to win a $50 cash prize. The chance of winning is 1 in 25.<br>
<h2>HOW WILL MY CONFIDENTIALITY BE PROTECTED?</h2><br>
All data collected for this study is confidential. <br>
<h2>WHOM SHOULD I CONTACT IF I HAVE QUESTIONS?</h2><br>
You may ask any questions about the research at any time. If you have questions about the research after you leave today you should contact the Principal Investigator Martina Rau at 608-262-0833.<br>
If you are not satisfied with response of research team, have more questions, or want to talk with someone about your rights as a research participant, you should contact the Education Research and Social &amp; Behavioral Science IRB Office at 608-263-2320.<br>
Your participation is completely voluntary. If you decide not to participate or to withdraw from the study it will have no effect on your grade in this class.
By clicking 'Proceed' below, you indicate that you have read this consent form, had an opportunity to ask any questions about your participation in this research and voluntarily consent to participate."""

def get_introduction_instruction2():
    """
    : return: string, the second introduction instruction
    """

    return """Please read carefully through the following description. You will need this information to solve the problems in the remainder of this hit.<br>&nbsp;<br>Atoms of elements are rarely found uncombined in nature. Instead they often stick together to form molecules. What makes atoms stick together is called <em>bonding</em>. You will encounter four ways to represent bonding: Lewis structure, ball-and-stick model,space-filling model and electrostatic potential map. <br>Lewis structures show how many electrons are shared between the atoms. <br>&nbsp;<h3>Lewis structure of carbon disulfide:</h3><br><img height="192" src="https://dl.dropboxusercontent.com/u/17446302/allmolecules/CS2/Lewis_CS2.jpg" width="207"><br>&nbsp;<br>Ball-and-stick  models show the shape of a molecule. They show bonded electron pairs as lines, but they do not show the non-bonded electrons. Ball-and-stick models use color to show the identity of the atoms.<br>&nbsp;<h3>Ball-and-stick model of carbon disulfide:</h3><br><img height="192" src="https://dl.dropboxusercontent.com/u/17446302/allmolecules/CS2/BS_CS2.jpg" width="206"><br>&nbsp;<br>Space-filling models show the space the atom's electron clouds occupy. Space-filling models use the same color code as ball-and-stick models to show atom identity. Space filling models do not show bonds or electrons. <br>&nbsp;<h3>Space-filling model of carbon disulfide:</h3><br><img height="192" src="https://dl.dropboxusercontent.com/u/17446302/allmolecules/CS2/SF_CS2.jpg" width="206"><br>&nbsp;<br>Electrostatic potential maps show information about the polarity of bonds and about the shape of molecules. Red of high electron density, blue indicates regions of low electron density and green indicates medium electron density. Electrostatic potential maps use color to indicate the polarity of the bond and the region to which the electrons are drawn (in red).<br>&nbsp;<h3>Electrostatic potential map of carbon disulfide:</h3><br><img height="192" src="https://dl.dropboxusercontent.com/u/17446302/allmolecules/CS2/EPM_CS2.jpg" width="206"><br>&nbsp;<br><h3>Electrostatic potential map of hydrogen chloride:</h3><br><img src="https://dl.dropboxusercontent.com/u/17446302/allmolecules/HCl/EPM_HCl.jpg" style="width: 203px; height: 192px;"><br>&nbsp;<br>In the following, you will be asked to judge whether two representations show the same molecule.&nbsp;<div><br></div><div>There are <b>126</b> questions in total. They are divided into three groups. The number of questions in the three groups are <b>21</b>, <b>63</b>&nbsp;and <b>42</b>&nbsp;respectively. To complete this survey you will need approximately <b>30-40 minutes</b>.<div>&nbsp;</div><div>"""
