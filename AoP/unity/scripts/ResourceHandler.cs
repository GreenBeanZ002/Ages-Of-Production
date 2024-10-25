using System.Collections;
using System.Collections.Generic;
using UnityEngine;


#region passivegain
public class ResourceHandler : MonoBehaviour
{
    #region resourceVariables
    public int NormalDelay = 1;
    public float NormalTimer = 0;
    public int Pop = 0;
    public int PopDelay = 1;
    public float PopTimer = 0;
    public int Gold = 1;
    public double GoldDelay = 0.05;
    public float GoldTimer = 0;
    public int GoldMult = 1;
    public int Wood = 0;
    #endregion
    #region buildingVariables
    public int resourcePrice_House = 10;
    #endregion



    void Update()
    {
        NormalTimer += Time.deltaTime;
        if (NormalTimer >= NormalDelay){
            NormalTimer = 0f;
            Wood++;
        }
        PopTimer += Time.deltaTime;
        if (PopTimer >= PopDelay)
        {
            PopTimer = 0f;
            Pop++;
        }
        GoldTimer += Time.deltaTime;
        if (GoldTimer >= GoldDelay)
        {
            GoldTimer = 0f;
            Gold += 1 * GoldMult;

        }
    }


}
#endregion

