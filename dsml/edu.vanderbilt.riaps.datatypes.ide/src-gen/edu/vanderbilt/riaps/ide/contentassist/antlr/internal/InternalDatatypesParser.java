package edu.vanderbilt.riaps.ide.contentassist.antlr.internal;

import java.io.InputStream;
import org.eclipse.xtext.*;
import org.eclipse.xtext.parser.*;
import org.eclipse.xtext.parser.impl.*;
import org.eclipse.emf.ecore.util.EcoreUtil;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.xtext.parser.antlr.XtextTokenStream;
import org.eclipse.xtext.parser.antlr.XtextTokenStream.HiddenTokens;
import org.eclipse.xtext.ide.editor.contentassist.antlr.internal.AbstractInternalContentAssistParser;
import org.eclipse.xtext.ide.editor.contentassist.antlr.internal.DFA;
import edu.vanderbilt.riaps.services.DatatypesGrammarAccess;



import org.antlr.runtime.*;
import java.util.Stack;
import java.util.List;
import java.util.ArrayList;

@SuppressWarnings("all")
public class InternalDatatypesParser extends AbstractInternalContentAssistParser {
    public static final String[] tokenNames = new String[] {
        "<invalid>", "<EOR>", "<DOWN>", "<UP>", "RULE_ID", "RULE_ANNOTATION_STRING", "RULE_INT", "RULE_STRING", "RULE_ML_COMMENT", "RULE_SL_COMMENT", "RULE_WS", "RULE_ANY_OTHER", "'Int8'", "'UInt8'", "'Int16'", "'UInt16'", "'Int32'", "'UInt32'", "'Int64'", "'UInt64'", "'Boolean'", "'String'", "'Float'", "'Double'", "'ByteBuffer'", "'package'", "'import'", "'.'", "'*'", "'<**'", "'**>'", "'typeCollection'", "'{'", "'}'", "'version'", "'messageCollection'", "'key'", "'major'", "'minor'", "'array'", "'of'", "'typedef'", "'is'", "'struct'", "'extends'", "'enumeration'", "','", "'='", "'map'", "'to'", "']'", "'['"
    };
    public static final int T__50=50;
    public static final int T__19=19;
    public static final int T__15=15;
    public static final int T__16=16;
    public static final int T__17=17;
    public static final int T__18=18;
    public static final int T__12=12;
    public static final int T__13=13;
    public static final int T__14=14;
    public static final int T__51=51;
    public static final int RULE_ID=4;
    public static final int T__26=26;
    public static final int T__27=27;
    public static final int T__28=28;
    public static final int RULE_INT=6;
    public static final int T__29=29;
    public static final int T__22=22;
    public static final int RULE_ML_COMMENT=8;
    public static final int T__23=23;
    public static final int T__24=24;
    public static final int T__25=25;
    public static final int T__20=20;
    public static final int T__21=21;
    public static final int RULE_STRING=7;
    public static final int RULE_SL_COMMENT=9;
    public static final int T__37=37;
    public static final int T__38=38;
    public static final int T__39=39;
    public static final int T__33=33;
    public static final int T__34=34;
    public static final int T__35=35;
    public static final int T__36=36;
    public static final int EOF=-1;
    public static final int T__30=30;
    public static final int T__31=31;
    public static final int RULE_ANNOTATION_STRING=5;
    public static final int T__32=32;
    public static final int RULE_WS=10;
    public static final int RULE_ANY_OTHER=11;
    public static final int T__48=48;
    public static final int T__49=49;
    public static final int T__44=44;
    public static final int T__45=45;
    public static final int T__46=46;
    public static final int T__47=47;
    public static final int T__40=40;
    public static final int T__41=41;
    public static final int T__42=42;
    public static final int T__43=43;

    // delegates
    // delegators


        public InternalDatatypesParser(TokenStream input) {
            this(input, new RecognizerSharedState());
        }
        public InternalDatatypesParser(TokenStream input, RecognizerSharedState state) {
            super(input, state);
             
        }
        

    public String[] getTokenNames() { return InternalDatatypesParser.tokenNames; }
    public String getGrammarFileName() { return "InternalDatatypes.g"; }


    	private DatatypesGrammarAccess grammarAccess;

    	public void setGrammarAccess(DatatypesGrammarAccess grammarAccess) {
    		this.grammarAccess = grammarAccess;
    	}

    	@Override
    	protected Grammar getGrammar() {
    		return grammarAccess.getGrammar();
    	}

    	@Override
    	protected String getValueForTokenName(String tokenName) {
    		return tokenName;
    	}



    // $ANTLR start "entryRuleModel"
    // InternalDatatypes.g:53:1: entryRuleModel : ruleModel EOF ;
    public final void entryRuleModel() throws RecognitionException {
        try {
            // InternalDatatypes.g:54:1: ( ruleModel EOF )
            // InternalDatatypes.g:55:1: ruleModel EOF
            {
             before(grammarAccess.getModelRule()); 
            pushFollow(FOLLOW_1);
            ruleModel();

            state._fsp--;

             after(grammarAccess.getModelRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleModel"


    // $ANTLR start "ruleModel"
    // InternalDatatypes.g:62:1: ruleModel : ( ( rule__Model__Group__0 ) ) ;
    public final void ruleModel() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:66:2: ( ( ( rule__Model__Group__0 ) ) )
            // InternalDatatypes.g:67:2: ( ( rule__Model__Group__0 ) )
            {
            // InternalDatatypes.g:67:2: ( ( rule__Model__Group__0 ) )
            // InternalDatatypes.g:68:3: ( rule__Model__Group__0 )
            {
             before(grammarAccess.getModelAccess().getGroup()); 
            // InternalDatatypes.g:69:3: ( rule__Model__Group__0 )
            // InternalDatatypes.g:69:4: rule__Model__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__Model__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getModelAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleModel"


    // $ANTLR start "entryRulePackage"
    // InternalDatatypes.g:78:1: entryRulePackage : rulePackage EOF ;
    public final void entryRulePackage() throws RecognitionException {
        try {
            // InternalDatatypes.g:79:1: ( rulePackage EOF )
            // InternalDatatypes.g:80:1: rulePackage EOF
            {
             before(grammarAccess.getPackageRule()); 
            pushFollow(FOLLOW_1);
            rulePackage();

            state._fsp--;

             after(grammarAccess.getPackageRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRulePackage"


    // $ANTLR start "rulePackage"
    // InternalDatatypes.g:87:1: rulePackage : ( ( rule__Package__Group__0 ) ) ;
    public final void rulePackage() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:91:2: ( ( ( rule__Package__Group__0 ) ) )
            // InternalDatatypes.g:92:2: ( ( rule__Package__Group__0 ) )
            {
            // InternalDatatypes.g:92:2: ( ( rule__Package__Group__0 ) )
            // InternalDatatypes.g:93:3: ( rule__Package__Group__0 )
            {
             before(grammarAccess.getPackageAccess().getGroup()); 
            // InternalDatatypes.g:94:3: ( rule__Package__Group__0 )
            // InternalDatatypes.g:94:4: rule__Package__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__Package__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getPackageAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rulePackage"


    // $ANTLR start "entryRuleImport"
    // InternalDatatypes.g:103:1: entryRuleImport : ruleImport EOF ;
    public final void entryRuleImport() throws RecognitionException {
        try {
            // InternalDatatypes.g:104:1: ( ruleImport EOF )
            // InternalDatatypes.g:105:1: ruleImport EOF
            {
             before(grammarAccess.getImportRule()); 
            pushFollow(FOLLOW_1);
            ruleImport();

            state._fsp--;

             after(grammarAccess.getImportRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleImport"


    // $ANTLR start "ruleImport"
    // InternalDatatypes.g:112:1: ruleImport : ( ( rule__Import__Group__0 ) ) ;
    public final void ruleImport() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:116:2: ( ( ( rule__Import__Group__0 ) ) )
            // InternalDatatypes.g:117:2: ( ( rule__Import__Group__0 ) )
            {
            // InternalDatatypes.g:117:2: ( ( rule__Import__Group__0 ) )
            // InternalDatatypes.g:118:3: ( rule__Import__Group__0 )
            {
             before(grammarAccess.getImportAccess().getGroup()); 
            // InternalDatatypes.g:119:3: ( rule__Import__Group__0 )
            // InternalDatatypes.g:119:4: rule__Import__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__Import__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getImportAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleImport"


    // $ANTLR start "entryRuleImportedFQN"
    // InternalDatatypes.g:128:1: entryRuleImportedFQN : ruleImportedFQN EOF ;
    public final void entryRuleImportedFQN() throws RecognitionException {
        try {
            // InternalDatatypes.g:129:1: ( ruleImportedFQN EOF )
            // InternalDatatypes.g:130:1: ruleImportedFQN EOF
            {
             before(grammarAccess.getImportedFQNRule()); 
            pushFollow(FOLLOW_1);
            ruleImportedFQN();

            state._fsp--;

             after(grammarAccess.getImportedFQNRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleImportedFQN"


    // $ANTLR start "ruleImportedFQN"
    // InternalDatatypes.g:137:1: ruleImportedFQN : ( ( rule__ImportedFQN__Group__0 ) ) ;
    public final void ruleImportedFQN() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:141:2: ( ( ( rule__ImportedFQN__Group__0 ) ) )
            // InternalDatatypes.g:142:2: ( ( rule__ImportedFQN__Group__0 ) )
            {
            // InternalDatatypes.g:142:2: ( ( rule__ImportedFQN__Group__0 ) )
            // InternalDatatypes.g:143:3: ( rule__ImportedFQN__Group__0 )
            {
             before(grammarAccess.getImportedFQNAccess().getGroup()); 
            // InternalDatatypes.g:144:3: ( rule__ImportedFQN__Group__0 )
            // InternalDatatypes.g:144:4: rule__ImportedFQN__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__ImportedFQN__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getImportedFQNAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleImportedFQN"


    // $ANTLR start "entryRuleFQN"
    // InternalDatatypes.g:153:1: entryRuleFQN : ruleFQN EOF ;
    public final void entryRuleFQN() throws RecognitionException {
        try {
            // InternalDatatypes.g:154:1: ( ruleFQN EOF )
            // InternalDatatypes.g:155:1: ruleFQN EOF
            {
             before(grammarAccess.getFQNRule()); 
            pushFollow(FOLLOW_1);
            ruleFQN();

            state._fsp--;

             after(grammarAccess.getFQNRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFQN"


    // $ANTLR start "ruleFQN"
    // InternalDatatypes.g:162:1: ruleFQN : ( ( rule__FQN__Group__0 ) ) ;
    public final void ruleFQN() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:166:2: ( ( ( rule__FQN__Group__0 ) ) )
            // InternalDatatypes.g:167:2: ( ( rule__FQN__Group__0 ) )
            {
            // InternalDatatypes.g:167:2: ( ( rule__FQN__Group__0 ) )
            // InternalDatatypes.g:168:3: ( rule__FQN__Group__0 )
            {
             before(grammarAccess.getFQNAccess().getGroup()); 
            // InternalDatatypes.g:169:3: ( rule__FQN__Group__0 )
            // InternalDatatypes.g:169:4: rule__FQN__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FQN__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFQNAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFQN"


    // $ANTLR start "entryRuleFAnnotationBlock"
    // InternalDatatypes.g:178:1: entryRuleFAnnotationBlock : ruleFAnnotationBlock EOF ;
    public final void entryRuleFAnnotationBlock() throws RecognitionException {
        try {
            // InternalDatatypes.g:179:1: ( ruleFAnnotationBlock EOF )
            // InternalDatatypes.g:180:1: ruleFAnnotationBlock EOF
            {
             before(grammarAccess.getFAnnotationBlockRule()); 
            pushFollow(FOLLOW_1);
            ruleFAnnotationBlock();

            state._fsp--;

             after(grammarAccess.getFAnnotationBlockRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFAnnotationBlock"


    // $ANTLR start "ruleFAnnotationBlock"
    // InternalDatatypes.g:187:1: ruleFAnnotationBlock : ( ( rule__FAnnotationBlock__Group__0 ) ) ;
    public final void ruleFAnnotationBlock() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:191:2: ( ( ( rule__FAnnotationBlock__Group__0 ) ) )
            // InternalDatatypes.g:192:2: ( ( rule__FAnnotationBlock__Group__0 ) )
            {
            // InternalDatatypes.g:192:2: ( ( rule__FAnnotationBlock__Group__0 ) )
            // InternalDatatypes.g:193:3: ( rule__FAnnotationBlock__Group__0 )
            {
             before(grammarAccess.getFAnnotationBlockAccess().getGroup()); 
            // InternalDatatypes.g:194:3: ( rule__FAnnotationBlock__Group__0 )
            // InternalDatatypes.g:194:4: rule__FAnnotationBlock__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FAnnotationBlock__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFAnnotationBlockAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFAnnotationBlock"


    // $ANTLR start "entryRuleFAnnotation"
    // InternalDatatypes.g:203:1: entryRuleFAnnotation : ruleFAnnotation EOF ;
    public final void entryRuleFAnnotation() throws RecognitionException {
        try {
            // InternalDatatypes.g:204:1: ( ruleFAnnotation EOF )
            // InternalDatatypes.g:205:1: ruleFAnnotation EOF
            {
             before(grammarAccess.getFAnnotationRule()); 
            pushFollow(FOLLOW_1);
            ruleFAnnotation();

            state._fsp--;

             after(grammarAccess.getFAnnotationRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFAnnotation"


    // $ANTLR start "ruleFAnnotation"
    // InternalDatatypes.g:212:1: ruleFAnnotation : ( ( rule__FAnnotation__RawTextAssignment ) ) ;
    public final void ruleFAnnotation() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:216:2: ( ( ( rule__FAnnotation__RawTextAssignment ) ) )
            // InternalDatatypes.g:217:2: ( ( rule__FAnnotation__RawTextAssignment ) )
            {
            // InternalDatatypes.g:217:2: ( ( rule__FAnnotation__RawTextAssignment ) )
            // InternalDatatypes.g:218:3: ( rule__FAnnotation__RawTextAssignment )
            {
             before(grammarAccess.getFAnnotationAccess().getRawTextAssignment()); 
            // InternalDatatypes.g:219:3: ( rule__FAnnotation__RawTextAssignment )
            // InternalDatatypes.g:219:4: rule__FAnnotation__RawTextAssignment
            {
            pushFollow(FOLLOW_2);
            rule__FAnnotation__RawTextAssignment();

            state._fsp--;


            }

             after(grammarAccess.getFAnnotationAccess().getRawTextAssignment()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFAnnotation"


    // $ANTLR start "entryRuleFTypeCollection"
    // InternalDatatypes.g:228:1: entryRuleFTypeCollection : ruleFTypeCollection EOF ;
    public final void entryRuleFTypeCollection() throws RecognitionException {
        try {
            // InternalDatatypes.g:229:1: ( ruleFTypeCollection EOF )
            // InternalDatatypes.g:230:1: ruleFTypeCollection EOF
            {
             before(grammarAccess.getFTypeCollectionRule()); 
            pushFollow(FOLLOW_1);
            ruleFTypeCollection();

            state._fsp--;

             after(grammarAccess.getFTypeCollectionRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFTypeCollection"


    // $ANTLR start "ruleFTypeCollection"
    // InternalDatatypes.g:237:1: ruleFTypeCollection : ( ( rule__FTypeCollection__Group__0 ) ) ;
    public final void ruleFTypeCollection() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:241:2: ( ( ( rule__FTypeCollection__Group__0 ) ) )
            // InternalDatatypes.g:242:2: ( ( rule__FTypeCollection__Group__0 ) )
            {
            // InternalDatatypes.g:242:2: ( ( rule__FTypeCollection__Group__0 ) )
            // InternalDatatypes.g:243:3: ( rule__FTypeCollection__Group__0 )
            {
             before(grammarAccess.getFTypeCollectionAccess().getGroup()); 
            // InternalDatatypes.g:244:3: ( rule__FTypeCollection__Group__0 )
            // InternalDatatypes.g:244:4: rule__FTypeCollection__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FTypeCollection__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFTypeCollectionAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFTypeCollection"


    // $ANTLR start "entryRuleFMessageCollection"
    // InternalDatatypes.g:253:1: entryRuleFMessageCollection : ruleFMessageCollection EOF ;
    public final void entryRuleFMessageCollection() throws RecognitionException {
        try {
            // InternalDatatypes.g:254:1: ( ruleFMessageCollection EOF )
            // InternalDatatypes.g:255:1: ruleFMessageCollection EOF
            {
             before(grammarAccess.getFMessageCollectionRule()); 
            pushFollow(FOLLOW_1);
            ruleFMessageCollection();

            state._fsp--;

             after(grammarAccess.getFMessageCollectionRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFMessageCollection"


    // $ANTLR start "ruleFMessageCollection"
    // InternalDatatypes.g:262:1: ruleFMessageCollection : ( ( rule__FMessageCollection__Group__0 ) ) ;
    public final void ruleFMessageCollection() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:266:2: ( ( ( rule__FMessageCollection__Group__0 ) ) )
            // InternalDatatypes.g:267:2: ( ( rule__FMessageCollection__Group__0 ) )
            {
            // InternalDatatypes.g:267:2: ( ( rule__FMessageCollection__Group__0 ) )
            // InternalDatatypes.g:268:3: ( rule__FMessageCollection__Group__0 )
            {
             before(grammarAccess.getFMessageCollectionAccess().getGroup()); 
            // InternalDatatypes.g:269:3: ( rule__FMessageCollection__Group__0 )
            // InternalDatatypes.g:269:4: rule__FMessageCollection__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FMessageCollection__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFMessageCollectionAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFMessageCollection"


    // $ANTLR start "entryRuleFMessage"
    // InternalDatatypes.g:278:1: entryRuleFMessage : ruleFMessage EOF ;
    public final void entryRuleFMessage() throws RecognitionException {
        try {
            // InternalDatatypes.g:279:1: ( ruleFMessage EOF )
            // InternalDatatypes.g:280:1: ruleFMessage EOF
            {
             before(grammarAccess.getFMessageRule()); 
            pushFollow(FOLLOW_1);
            ruleFMessage();

            state._fsp--;

             after(grammarAccess.getFMessageRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFMessage"


    // $ANTLR start "ruleFMessage"
    // InternalDatatypes.g:287:1: ruleFMessage : ( ( rule__FMessage__Group__0 ) ) ;
    public final void ruleFMessage() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:291:2: ( ( ( rule__FMessage__Group__0 ) ) )
            // InternalDatatypes.g:292:2: ( ( rule__FMessage__Group__0 ) )
            {
            // InternalDatatypes.g:292:2: ( ( rule__FMessage__Group__0 ) )
            // InternalDatatypes.g:293:3: ( rule__FMessage__Group__0 )
            {
             before(grammarAccess.getFMessageAccess().getGroup()); 
            // InternalDatatypes.g:294:3: ( rule__FMessage__Group__0 )
            // InternalDatatypes.g:294:4: rule__FMessage__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FMessage__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFMessageAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFMessage"


    // $ANTLR start "entryRuleFVersion"
    // InternalDatatypes.g:303:1: entryRuleFVersion : ruleFVersion EOF ;
    public final void entryRuleFVersion() throws RecognitionException {
        try {
            // InternalDatatypes.g:304:1: ( ruleFVersion EOF )
            // InternalDatatypes.g:305:1: ruleFVersion EOF
            {
             before(grammarAccess.getFVersionRule()); 
            pushFollow(FOLLOW_1);
            ruleFVersion();

            state._fsp--;

             after(grammarAccess.getFVersionRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFVersion"


    // $ANTLR start "ruleFVersion"
    // InternalDatatypes.g:312:1: ruleFVersion : ( ( rule__FVersion__Group__0 ) ) ;
    public final void ruleFVersion() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:316:2: ( ( ( rule__FVersion__Group__0 ) ) )
            // InternalDatatypes.g:317:2: ( ( rule__FVersion__Group__0 ) )
            {
            // InternalDatatypes.g:317:2: ( ( rule__FVersion__Group__0 ) )
            // InternalDatatypes.g:318:3: ( rule__FVersion__Group__0 )
            {
             before(grammarAccess.getFVersionAccess().getGroup()); 
            // InternalDatatypes.g:319:3: ( rule__FVersion__Group__0 )
            // InternalDatatypes.g:319:4: rule__FVersion__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FVersion__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFVersionAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFVersion"


    // $ANTLR start "entryRuleFTypeRef"
    // InternalDatatypes.g:328:1: entryRuleFTypeRef : ruleFTypeRef EOF ;
    public final void entryRuleFTypeRef() throws RecognitionException {
        try {
            // InternalDatatypes.g:329:1: ( ruleFTypeRef EOF )
            // InternalDatatypes.g:330:1: ruleFTypeRef EOF
            {
             before(grammarAccess.getFTypeRefRule()); 
            pushFollow(FOLLOW_1);
            ruleFTypeRef();

            state._fsp--;

             after(grammarAccess.getFTypeRefRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFTypeRef"


    // $ANTLR start "ruleFTypeRef"
    // InternalDatatypes.g:337:1: ruleFTypeRef : ( ( rule__FTypeRef__Alternatives ) ) ;
    public final void ruleFTypeRef() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:341:2: ( ( ( rule__FTypeRef__Alternatives ) ) )
            // InternalDatatypes.g:342:2: ( ( rule__FTypeRef__Alternatives ) )
            {
            // InternalDatatypes.g:342:2: ( ( rule__FTypeRef__Alternatives ) )
            // InternalDatatypes.g:343:3: ( rule__FTypeRef__Alternatives )
            {
             before(grammarAccess.getFTypeRefAccess().getAlternatives()); 
            // InternalDatatypes.g:344:3: ( rule__FTypeRef__Alternatives )
            // InternalDatatypes.g:344:4: rule__FTypeRef__Alternatives
            {
            pushFollow(FOLLOW_2);
            rule__FTypeRef__Alternatives();

            state._fsp--;


            }

             after(grammarAccess.getFTypeRefAccess().getAlternatives()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFTypeRef"


    // $ANTLR start "entryRuleFType"
    // InternalDatatypes.g:353:1: entryRuleFType : ruleFType EOF ;
    public final void entryRuleFType() throws RecognitionException {
        try {
            // InternalDatatypes.g:354:1: ( ruleFType EOF )
            // InternalDatatypes.g:355:1: ruleFType EOF
            {
             before(grammarAccess.getFTypeRule()); 
            pushFollow(FOLLOW_1);
            ruleFType();

            state._fsp--;

             after(grammarAccess.getFTypeRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFType"


    // $ANTLR start "ruleFType"
    // InternalDatatypes.g:362:1: ruleFType : ( ( rule__FType__Alternatives ) ) ;
    public final void ruleFType() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:366:2: ( ( ( rule__FType__Alternatives ) ) )
            // InternalDatatypes.g:367:2: ( ( rule__FType__Alternatives ) )
            {
            // InternalDatatypes.g:367:2: ( ( rule__FType__Alternatives ) )
            // InternalDatatypes.g:368:3: ( rule__FType__Alternatives )
            {
             before(grammarAccess.getFTypeAccess().getAlternatives()); 
            // InternalDatatypes.g:369:3: ( rule__FType__Alternatives )
            // InternalDatatypes.g:369:4: rule__FType__Alternatives
            {
            pushFollow(FOLLOW_2);
            rule__FType__Alternatives();

            state._fsp--;


            }

             after(grammarAccess.getFTypeAccess().getAlternatives()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFType"


    // $ANTLR start "entryRuleFArrayType"
    // InternalDatatypes.g:378:1: entryRuleFArrayType : ruleFArrayType EOF ;
    public final void entryRuleFArrayType() throws RecognitionException {
        try {
            // InternalDatatypes.g:379:1: ( ruleFArrayType EOF )
            // InternalDatatypes.g:380:1: ruleFArrayType EOF
            {
             before(grammarAccess.getFArrayTypeRule()); 
            pushFollow(FOLLOW_1);
            ruleFArrayType();

            state._fsp--;

             after(grammarAccess.getFArrayTypeRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFArrayType"


    // $ANTLR start "ruleFArrayType"
    // InternalDatatypes.g:387:1: ruleFArrayType : ( ( rule__FArrayType__Group__0 ) ) ;
    public final void ruleFArrayType() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:391:2: ( ( ( rule__FArrayType__Group__0 ) ) )
            // InternalDatatypes.g:392:2: ( ( rule__FArrayType__Group__0 ) )
            {
            // InternalDatatypes.g:392:2: ( ( rule__FArrayType__Group__0 ) )
            // InternalDatatypes.g:393:3: ( rule__FArrayType__Group__0 )
            {
             before(grammarAccess.getFArrayTypeAccess().getGroup()); 
            // InternalDatatypes.g:394:3: ( rule__FArrayType__Group__0 )
            // InternalDatatypes.g:394:4: rule__FArrayType__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FArrayType__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFArrayTypeAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFArrayType"


    // $ANTLR start "entryRuleFTypeDef"
    // InternalDatatypes.g:403:1: entryRuleFTypeDef : ruleFTypeDef EOF ;
    public final void entryRuleFTypeDef() throws RecognitionException {
        try {
            // InternalDatatypes.g:404:1: ( ruleFTypeDef EOF )
            // InternalDatatypes.g:405:1: ruleFTypeDef EOF
            {
             before(grammarAccess.getFTypeDefRule()); 
            pushFollow(FOLLOW_1);
            ruleFTypeDef();

            state._fsp--;

             after(grammarAccess.getFTypeDefRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFTypeDef"


    // $ANTLR start "ruleFTypeDef"
    // InternalDatatypes.g:412:1: ruleFTypeDef : ( ( rule__FTypeDef__Group__0 ) ) ;
    public final void ruleFTypeDef() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:416:2: ( ( ( rule__FTypeDef__Group__0 ) ) )
            // InternalDatatypes.g:417:2: ( ( rule__FTypeDef__Group__0 ) )
            {
            // InternalDatatypes.g:417:2: ( ( rule__FTypeDef__Group__0 ) )
            // InternalDatatypes.g:418:3: ( rule__FTypeDef__Group__0 )
            {
             before(grammarAccess.getFTypeDefAccess().getGroup()); 
            // InternalDatatypes.g:419:3: ( rule__FTypeDef__Group__0 )
            // InternalDatatypes.g:419:4: rule__FTypeDef__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FTypeDef__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFTypeDefAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFTypeDef"


    // $ANTLR start "entryRuleFStructType"
    // InternalDatatypes.g:428:1: entryRuleFStructType : ruleFStructType EOF ;
    public final void entryRuleFStructType() throws RecognitionException {
        try {
            // InternalDatatypes.g:429:1: ( ruleFStructType EOF )
            // InternalDatatypes.g:430:1: ruleFStructType EOF
            {
             before(grammarAccess.getFStructTypeRule()); 
            pushFollow(FOLLOW_1);
            ruleFStructType();

            state._fsp--;

             after(grammarAccess.getFStructTypeRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFStructType"


    // $ANTLR start "ruleFStructType"
    // InternalDatatypes.g:437:1: ruleFStructType : ( ( rule__FStructType__Group__0 ) ) ;
    public final void ruleFStructType() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:441:2: ( ( ( rule__FStructType__Group__0 ) ) )
            // InternalDatatypes.g:442:2: ( ( rule__FStructType__Group__0 ) )
            {
            // InternalDatatypes.g:442:2: ( ( rule__FStructType__Group__0 ) )
            // InternalDatatypes.g:443:3: ( rule__FStructType__Group__0 )
            {
             before(grammarAccess.getFStructTypeAccess().getGroup()); 
            // InternalDatatypes.g:444:3: ( rule__FStructType__Group__0 )
            // InternalDatatypes.g:444:4: rule__FStructType__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FStructType__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFStructTypeAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFStructType"


    // $ANTLR start "entryRuleFEnumerationType"
    // InternalDatatypes.g:453:1: entryRuleFEnumerationType : ruleFEnumerationType EOF ;
    public final void entryRuleFEnumerationType() throws RecognitionException {
        try {
            // InternalDatatypes.g:454:1: ( ruleFEnumerationType EOF )
            // InternalDatatypes.g:455:1: ruleFEnumerationType EOF
            {
             before(grammarAccess.getFEnumerationTypeRule()); 
            pushFollow(FOLLOW_1);
            ruleFEnumerationType();

            state._fsp--;

             after(grammarAccess.getFEnumerationTypeRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFEnumerationType"


    // $ANTLR start "ruleFEnumerationType"
    // InternalDatatypes.g:462:1: ruleFEnumerationType : ( ( rule__FEnumerationType__Group__0 ) ) ;
    public final void ruleFEnumerationType() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:466:2: ( ( ( rule__FEnumerationType__Group__0 ) ) )
            // InternalDatatypes.g:467:2: ( ( rule__FEnumerationType__Group__0 ) )
            {
            // InternalDatatypes.g:467:2: ( ( rule__FEnumerationType__Group__0 ) )
            // InternalDatatypes.g:468:3: ( rule__FEnumerationType__Group__0 )
            {
             before(grammarAccess.getFEnumerationTypeAccess().getGroup()); 
            // InternalDatatypes.g:469:3: ( rule__FEnumerationType__Group__0 )
            // InternalDatatypes.g:469:4: rule__FEnumerationType__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFEnumerationTypeAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFEnumerationType"


    // $ANTLR start "entryRuleFEnumerator"
    // InternalDatatypes.g:478:1: entryRuleFEnumerator : ruleFEnumerator EOF ;
    public final void entryRuleFEnumerator() throws RecognitionException {
        try {
            // InternalDatatypes.g:479:1: ( ruleFEnumerator EOF )
            // InternalDatatypes.g:480:1: ruleFEnumerator EOF
            {
             before(grammarAccess.getFEnumeratorRule()); 
            pushFollow(FOLLOW_1);
            ruleFEnumerator();

            state._fsp--;

             after(grammarAccess.getFEnumeratorRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFEnumerator"


    // $ANTLR start "ruleFEnumerator"
    // InternalDatatypes.g:487:1: ruleFEnumerator : ( ( rule__FEnumerator__Group__0 ) ) ;
    public final void ruleFEnumerator() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:491:2: ( ( ( rule__FEnumerator__Group__0 ) ) )
            // InternalDatatypes.g:492:2: ( ( rule__FEnumerator__Group__0 ) )
            {
            // InternalDatatypes.g:492:2: ( ( rule__FEnumerator__Group__0 ) )
            // InternalDatatypes.g:493:3: ( rule__FEnumerator__Group__0 )
            {
             before(grammarAccess.getFEnumeratorAccess().getGroup()); 
            // InternalDatatypes.g:494:3: ( rule__FEnumerator__Group__0 )
            // InternalDatatypes.g:494:4: rule__FEnumerator__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerator__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFEnumeratorAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFEnumerator"


    // $ANTLR start "entryRuleFMapType"
    // InternalDatatypes.g:503:1: entryRuleFMapType : ruleFMapType EOF ;
    public final void entryRuleFMapType() throws RecognitionException {
        try {
            // InternalDatatypes.g:504:1: ( ruleFMapType EOF )
            // InternalDatatypes.g:505:1: ruleFMapType EOF
            {
             before(grammarAccess.getFMapTypeRule()); 
            pushFollow(FOLLOW_1);
            ruleFMapType();

            state._fsp--;

             after(grammarAccess.getFMapTypeRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFMapType"


    // $ANTLR start "ruleFMapType"
    // InternalDatatypes.g:512:1: ruleFMapType : ( ( rule__FMapType__Group__0 ) ) ;
    public final void ruleFMapType() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:516:2: ( ( ( rule__FMapType__Group__0 ) ) )
            // InternalDatatypes.g:517:2: ( ( rule__FMapType__Group__0 ) )
            {
            // InternalDatatypes.g:517:2: ( ( rule__FMapType__Group__0 ) )
            // InternalDatatypes.g:518:3: ( rule__FMapType__Group__0 )
            {
             before(grammarAccess.getFMapTypeAccess().getGroup()); 
            // InternalDatatypes.g:519:3: ( rule__FMapType__Group__0 )
            // InternalDatatypes.g:519:4: rule__FMapType__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FMapType__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFMapTypeAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFMapType"


    // $ANTLR start "entryRuleFField"
    // InternalDatatypes.g:528:1: entryRuleFField : ruleFField EOF ;
    public final void entryRuleFField() throws RecognitionException {
        try {
            // InternalDatatypes.g:529:1: ( ruleFField EOF )
            // InternalDatatypes.g:530:1: ruleFField EOF
            {
             before(grammarAccess.getFFieldRule()); 
            pushFollow(FOLLOW_1);
            ruleFField();

            state._fsp--;

             after(grammarAccess.getFFieldRule()); 
            match(input,EOF,FOLLOW_2); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "entryRuleFField"


    // $ANTLR start "ruleFField"
    // InternalDatatypes.g:537:1: ruleFField : ( ( rule__FField__Group__0 ) ) ;
    public final void ruleFField() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:541:2: ( ( ( rule__FField__Group__0 ) ) )
            // InternalDatatypes.g:542:2: ( ( rule__FField__Group__0 ) )
            {
            // InternalDatatypes.g:542:2: ( ( rule__FField__Group__0 ) )
            // InternalDatatypes.g:543:3: ( rule__FField__Group__0 )
            {
             before(grammarAccess.getFFieldAccess().getGroup()); 
            // InternalDatatypes.g:544:3: ( rule__FField__Group__0 )
            // InternalDatatypes.g:544:4: rule__FField__Group__0
            {
            pushFollow(FOLLOW_2);
            rule__FField__Group__0();

            state._fsp--;


            }

             after(grammarAccess.getFFieldAccess().getGroup()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFField"


    // $ANTLR start "ruleFBasicTypeId"
    // InternalDatatypes.g:553:1: ruleFBasicTypeId : ( ( rule__FBasicTypeId__Alternatives ) ) ;
    public final void ruleFBasicTypeId() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:557:1: ( ( ( rule__FBasicTypeId__Alternatives ) ) )
            // InternalDatatypes.g:558:2: ( ( rule__FBasicTypeId__Alternatives ) )
            {
            // InternalDatatypes.g:558:2: ( ( rule__FBasicTypeId__Alternatives ) )
            // InternalDatatypes.g:559:3: ( rule__FBasicTypeId__Alternatives )
            {
             before(grammarAccess.getFBasicTypeIdAccess().getAlternatives()); 
            // InternalDatatypes.g:560:3: ( rule__FBasicTypeId__Alternatives )
            // InternalDatatypes.g:560:4: rule__FBasicTypeId__Alternatives
            {
            pushFollow(FOLLOW_2);
            rule__FBasicTypeId__Alternatives();

            state._fsp--;


            }

             after(grammarAccess.getFBasicTypeIdAccess().getAlternatives()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "ruleFBasicTypeId"


    // $ANTLR start "rule__Model__Alternatives_3"
    // InternalDatatypes.g:568:1: rule__Model__Alternatives_3 : ( ( ( rule__Model__TypeCollectionsAssignment_3_0 ) ) | ( ( rule__Model__MessageCollectionsAssignment_3_1 ) ) );
    public final void rule__Model__Alternatives_3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:572:1: ( ( ( rule__Model__TypeCollectionsAssignment_3_0 ) ) | ( ( rule__Model__MessageCollectionsAssignment_3_1 ) ) )
            int alt1=2;
            alt1 = dfa1.predict(input);
            switch (alt1) {
                case 1 :
                    // InternalDatatypes.g:573:2: ( ( rule__Model__TypeCollectionsAssignment_3_0 ) )
                    {
                    // InternalDatatypes.g:573:2: ( ( rule__Model__TypeCollectionsAssignment_3_0 ) )
                    // InternalDatatypes.g:574:3: ( rule__Model__TypeCollectionsAssignment_3_0 )
                    {
                     before(grammarAccess.getModelAccess().getTypeCollectionsAssignment_3_0()); 
                    // InternalDatatypes.g:575:3: ( rule__Model__TypeCollectionsAssignment_3_0 )
                    // InternalDatatypes.g:575:4: rule__Model__TypeCollectionsAssignment_3_0
                    {
                    pushFollow(FOLLOW_2);
                    rule__Model__TypeCollectionsAssignment_3_0();

                    state._fsp--;


                    }

                     after(grammarAccess.getModelAccess().getTypeCollectionsAssignment_3_0()); 

                    }


                    }
                    break;
                case 2 :
                    // InternalDatatypes.g:579:2: ( ( rule__Model__MessageCollectionsAssignment_3_1 ) )
                    {
                    // InternalDatatypes.g:579:2: ( ( rule__Model__MessageCollectionsAssignment_3_1 ) )
                    // InternalDatatypes.g:580:3: ( rule__Model__MessageCollectionsAssignment_3_1 )
                    {
                     before(grammarAccess.getModelAccess().getMessageCollectionsAssignment_3_1()); 
                    // InternalDatatypes.g:581:3: ( rule__Model__MessageCollectionsAssignment_3_1 )
                    // InternalDatatypes.g:581:4: rule__Model__MessageCollectionsAssignment_3_1
                    {
                    pushFollow(FOLLOW_2);
                    rule__Model__MessageCollectionsAssignment_3_1();

                    state._fsp--;


                    }

                     after(grammarAccess.getModelAccess().getMessageCollectionsAssignment_3_1()); 

                    }


                    }
                    break;

            }
        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__Alternatives_3"


    // $ANTLR start "rule__FTypeRef__Alternatives"
    // InternalDatatypes.g:589:1: rule__FTypeRef__Alternatives : ( ( ( rule__FTypeRef__PredefinedAssignment_0 ) ) | ( ( rule__FTypeRef__DerivedAssignment_1 ) ) );
    public final void rule__FTypeRef__Alternatives() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:593:1: ( ( ( rule__FTypeRef__PredefinedAssignment_0 ) ) | ( ( rule__FTypeRef__DerivedAssignment_1 ) ) )
            int alt2=2;
            int LA2_0 = input.LA(1);

            if ( ((LA2_0>=12 && LA2_0<=24)) ) {
                alt2=1;
            }
            else if ( (LA2_0==RULE_ID) ) {
                alt2=2;
            }
            else {
                NoViableAltException nvae =
                    new NoViableAltException("", 2, 0, input);

                throw nvae;
            }
            switch (alt2) {
                case 1 :
                    // InternalDatatypes.g:594:2: ( ( rule__FTypeRef__PredefinedAssignment_0 ) )
                    {
                    // InternalDatatypes.g:594:2: ( ( rule__FTypeRef__PredefinedAssignment_0 ) )
                    // InternalDatatypes.g:595:3: ( rule__FTypeRef__PredefinedAssignment_0 )
                    {
                     before(grammarAccess.getFTypeRefAccess().getPredefinedAssignment_0()); 
                    // InternalDatatypes.g:596:3: ( rule__FTypeRef__PredefinedAssignment_0 )
                    // InternalDatatypes.g:596:4: rule__FTypeRef__PredefinedAssignment_0
                    {
                    pushFollow(FOLLOW_2);
                    rule__FTypeRef__PredefinedAssignment_0();

                    state._fsp--;


                    }

                     after(grammarAccess.getFTypeRefAccess().getPredefinedAssignment_0()); 

                    }


                    }
                    break;
                case 2 :
                    // InternalDatatypes.g:600:2: ( ( rule__FTypeRef__DerivedAssignment_1 ) )
                    {
                    // InternalDatatypes.g:600:2: ( ( rule__FTypeRef__DerivedAssignment_1 ) )
                    // InternalDatatypes.g:601:3: ( rule__FTypeRef__DerivedAssignment_1 )
                    {
                     before(grammarAccess.getFTypeRefAccess().getDerivedAssignment_1()); 
                    // InternalDatatypes.g:602:3: ( rule__FTypeRef__DerivedAssignment_1 )
                    // InternalDatatypes.g:602:4: rule__FTypeRef__DerivedAssignment_1
                    {
                    pushFollow(FOLLOW_2);
                    rule__FTypeRef__DerivedAssignment_1();

                    state._fsp--;


                    }

                     after(grammarAccess.getFTypeRefAccess().getDerivedAssignment_1()); 

                    }


                    }
                    break;

            }
        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeRef__Alternatives"


    // $ANTLR start "rule__FType__Alternatives"
    // InternalDatatypes.g:610:1: rule__FType__Alternatives : ( ( ruleFArrayType ) | ( ruleFEnumerationType ) | ( ruleFStructType ) | ( ruleFMapType ) | ( ruleFTypeDef ) );
    public final void rule__FType__Alternatives() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:614:1: ( ( ruleFArrayType ) | ( ruleFEnumerationType ) | ( ruleFStructType ) | ( ruleFMapType ) | ( ruleFTypeDef ) )
            int alt3=5;
            alt3 = dfa3.predict(input);
            switch (alt3) {
                case 1 :
                    // InternalDatatypes.g:615:2: ( ruleFArrayType )
                    {
                    // InternalDatatypes.g:615:2: ( ruleFArrayType )
                    // InternalDatatypes.g:616:3: ruleFArrayType
                    {
                     before(grammarAccess.getFTypeAccess().getFArrayTypeParserRuleCall_0()); 
                    pushFollow(FOLLOW_2);
                    ruleFArrayType();

                    state._fsp--;

                     after(grammarAccess.getFTypeAccess().getFArrayTypeParserRuleCall_0()); 

                    }


                    }
                    break;
                case 2 :
                    // InternalDatatypes.g:621:2: ( ruleFEnumerationType )
                    {
                    // InternalDatatypes.g:621:2: ( ruleFEnumerationType )
                    // InternalDatatypes.g:622:3: ruleFEnumerationType
                    {
                     before(grammarAccess.getFTypeAccess().getFEnumerationTypeParserRuleCall_1()); 
                    pushFollow(FOLLOW_2);
                    ruleFEnumerationType();

                    state._fsp--;

                     after(grammarAccess.getFTypeAccess().getFEnumerationTypeParserRuleCall_1()); 

                    }


                    }
                    break;
                case 3 :
                    // InternalDatatypes.g:627:2: ( ruleFStructType )
                    {
                    // InternalDatatypes.g:627:2: ( ruleFStructType )
                    // InternalDatatypes.g:628:3: ruleFStructType
                    {
                     before(grammarAccess.getFTypeAccess().getFStructTypeParserRuleCall_2()); 
                    pushFollow(FOLLOW_2);
                    ruleFStructType();

                    state._fsp--;

                     after(grammarAccess.getFTypeAccess().getFStructTypeParserRuleCall_2()); 

                    }


                    }
                    break;
                case 4 :
                    // InternalDatatypes.g:633:2: ( ruleFMapType )
                    {
                    // InternalDatatypes.g:633:2: ( ruleFMapType )
                    // InternalDatatypes.g:634:3: ruleFMapType
                    {
                     before(grammarAccess.getFTypeAccess().getFMapTypeParserRuleCall_3()); 
                    pushFollow(FOLLOW_2);
                    ruleFMapType();

                    state._fsp--;

                     after(grammarAccess.getFTypeAccess().getFMapTypeParserRuleCall_3()); 

                    }


                    }
                    break;
                case 5 :
                    // InternalDatatypes.g:639:2: ( ruleFTypeDef )
                    {
                    // InternalDatatypes.g:639:2: ( ruleFTypeDef )
                    // InternalDatatypes.g:640:3: ruleFTypeDef
                    {
                     before(grammarAccess.getFTypeAccess().getFTypeDefParserRuleCall_4()); 
                    pushFollow(FOLLOW_2);
                    ruleFTypeDef();

                    state._fsp--;

                     after(grammarAccess.getFTypeAccess().getFTypeDefParserRuleCall_4()); 

                    }


                    }
                    break;

            }
        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FType__Alternatives"


    // $ANTLR start "rule__FBasicTypeId__Alternatives"
    // InternalDatatypes.g:649:1: rule__FBasicTypeId__Alternatives : ( ( ( 'Int8' ) ) | ( ( 'UInt8' ) ) | ( ( 'Int16' ) ) | ( ( 'UInt16' ) ) | ( ( 'Int32' ) ) | ( ( 'UInt32' ) ) | ( ( 'Int64' ) ) | ( ( 'UInt64' ) ) | ( ( 'Boolean' ) ) | ( ( 'String' ) ) | ( ( 'Float' ) ) | ( ( 'Double' ) ) | ( ( 'ByteBuffer' ) ) );
    public final void rule__FBasicTypeId__Alternatives() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:653:1: ( ( ( 'Int8' ) ) | ( ( 'UInt8' ) ) | ( ( 'Int16' ) ) | ( ( 'UInt16' ) ) | ( ( 'Int32' ) ) | ( ( 'UInt32' ) ) | ( ( 'Int64' ) ) | ( ( 'UInt64' ) ) | ( ( 'Boolean' ) ) | ( ( 'String' ) ) | ( ( 'Float' ) ) | ( ( 'Double' ) ) | ( ( 'ByteBuffer' ) ) )
            int alt4=13;
            switch ( input.LA(1) ) {
            case 12:
                {
                alt4=1;
                }
                break;
            case 13:
                {
                alt4=2;
                }
                break;
            case 14:
                {
                alt4=3;
                }
                break;
            case 15:
                {
                alt4=4;
                }
                break;
            case 16:
                {
                alt4=5;
                }
                break;
            case 17:
                {
                alt4=6;
                }
                break;
            case 18:
                {
                alt4=7;
                }
                break;
            case 19:
                {
                alt4=8;
                }
                break;
            case 20:
                {
                alt4=9;
                }
                break;
            case 21:
                {
                alt4=10;
                }
                break;
            case 22:
                {
                alt4=11;
                }
                break;
            case 23:
                {
                alt4=12;
                }
                break;
            case 24:
                {
                alt4=13;
                }
                break;
            default:
                NoViableAltException nvae =
                    new NoViableAltException("", 4, 0, input);

                throw nvae;
            }

            switch (alt4) {
                case 1 :
                    // InternalDatatypes.g:654:2: ( ( 'Int8' ) )
                    {
                    // InternalDatatypes.g:654:2: ( ( 'Int8' ) )
                    // InternalDatatypes.g:655:3: ( 'Int8' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getInt8EnumLiteralDeclaration_0()); 
                    // InternalDatatypes.g:656:3: ( 'Int8' )
                    // InternalDatatypes.g:656:4: 'Int8'
                    {
                    match(input,12,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getInt8EnumLiteralDeclaration_0()); 

                    }


                    }
                    break;
                case 2 :
                    // InternalDatatypes.g:660:2: ( ( 'UInt8' ) )
                    {
                    // InternalDatatypes.g:660:2: ( ( 'UInt8' ) )
                    // InternalDatatypes.g:661:3: ( 'UInt8' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getUInt8EnumLiteralDeclaration_1()); 
                    // InternalDatatypes.g:662:3: ( 'UInt8' )
                    // InternalDatatypes.g:662:4: 'UInt8'
                    {
                    match(input,13,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getUInt8EnumLiteralDeclaration_1()); 

                    }


                    }
                    break;
                case 3 :
                    // InternalDatatypes.g:666:2: ( ( 'Int16' ) )
                    {
                    // InternalDatatypes.g:666:2: ( ( 'Int16' ) )
                    // InternalDatatypes.g:667:3: ( 'Int16' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getInt16EnumLiteralDeclaration_2()); 
                    // InternalDatatypes.g:668:3: ( 'Int16' )
                    // InternalDatatypes.g:668:4: 'Int16'
                    {
                    match(input,14,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getInt16EnumLiteralDeclaration_2()); 

                    }


                    }
                    break;
                case 4 :
                    // InternalDatatypes.g:672:2: ( ( 'UInt16' ) )
                    {
                    // InternalDatatypes.g:672:2: ( ( 'UInt16' ) )
                    // InternalDatatypes.g:673:3: ( 'UInt16' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getUInt16EnumLiteralDeclaration_3()); 
                    // InternalDatatypes.g:674:3: ( 'UInt16' )
                    // InternalDatatypes.g:674:4: 'UInt16'
                    {
                    match(input,15,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getUInt16EnumLiteralDeclaration_3()); 

                    }


                    }
                    break;
                case 5 :
                    // InternalDatatypes.g:678:2: ( ( 'Int32' ) )
                    {
                    // InternalDatatypes.g:678:2: ( ( 'Int32' ) )
                    // InternalDatatypes.g:679:3: ( 'Int32' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getInt32EnumLiteralDeclaration_4()); 
                    // InternalDatatypes.g:680:3: ( 'Int32' )
                    // InternalDatatypes.g:680:4: 'Int32'
                    {
                    match(input,16,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getInt32EnumLiteralDeclaration_4()); 

                    }


                    }
                    break;
                case 6 :
                    // InternalDatatypes.g:684:2: ( ( 'UInt32' ) )
                    {
                    // InternalDatatypes.g:684:2: ( ( 'UInt32' ) )
                    // InternalDatatypes.g:685:3: ( 'UInt32' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getUInt32EnumLiteralDeclaration_5()); 
                    // InternalDatatypes.g:686:3: ( 'UInt32' )
                    // InternalDatatypes.g:686:4: 'UInt32'
                    {
                    match(input,17,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getUInt32EnumLiteralDeclaration_5()); 

                    }


                    }
                    break;
                case 7 :
                    // InternalDatatypes.g:690:2: ( ( 'Int64' ) )
                    {
                    // InternalDatatypes.g:690:2: ( ( 'Int64' ) )
                    // InternalDatatypes.g:691:3: ( 'Int64' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getInt64EnumLiteralDeclaration_6()); 
                    // InternalDatatypes.g:692:3: ( 'Int64' )
                    // InternalDatatypes.g:692:4: 'Int64'
                    {
                    match(input,18,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getInt64EnumLiteralDeclaration_6()); 

                    }


                    }
                    break;
                case 8 :
                    // InternalDatatypes.g:696:2: ( ( 'UInt64' ) )
                    {
                    // InternalDatatypes.g:696:2: ( ( 'UInt64' ) )
                    // InternalDatatypes.g:697:3: ( 'UInt64' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getUInt64EnumLiteralDeclaration_7()); 
                    // InternalDatatypes.g:698:3: ( 'UInt64' )
                    // InternalDatatypes.g:698:4: 'UInt64'
                    {
                    match(input,19,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getUInt64EnumLiteralDeclaration_7()); 

                    }


                    }
                    break;
                case 9 :
                    // InternalDatatypes.g:702:2: ( ( 'Boolean' ) )
                    {
                    // InternalDatatypes.g:702:2: ( ( 'Boolean' ) )
                    // InternalDatatypes.g:703:3: ( 'Boolean' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getBooleanEnumLiteralDeclaration_8()); 
                    // InternalDatatypes.g:704:3: ( 'Boolean' )
                    // InternalDatatypes.g:704:4: 'Boolean'
                    {
                    match(input,20,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getBooleanEnumLiteralDeclaration_8()); 

                    }


                    }
                    break;
                case 10 :
                    // InternalDatatypes.g:708:2: ( ( 'String' ) )
                    {
                    // InternalDatatypes.g:708:2: ( ( 'String' ) )
                    // InternalDatatypes.g:709:3: ( 'String' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getStringEnumLiteralDeclaration_9()); 
                    // InternalDatatypes.g:710:3: ( 'String' )
                    // InternalDatatypes.g:710:4: 'String'
                    {
                    match(input,21,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getStringEnumLiteralDeclaration_9()); 

                    }


                    }
                    break;
                case 11 :
                    // InternalDatatypes.g:714:2: ( ( 'Float' ) )
                    {
                    // InternalDatatypes.g:714:2: ( ( 'Float' ) )
                    // InternalDatatypes.g:715:3: ( 'Float' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getFloatEnumLiteralDeclaration_10()); 
                    // InternalDatatypes.g:716:3: ( 'Float' )
                    // InternalDatatypes.g:716:4: 'Float'
                    {
                    match(input,22,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getFloatEnumLiteralDeclaration_10()); 

                    }


                    }
                    break;
                case 12 :
                    // InternalDatatypes.g:720:2: ( ( 'Double' ) )
                    {
                    // InternalDatatypes.g:720:2: ( ( 'Double' ) )
                    // InternalDatatypes.g:721:3: ( 'Double' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getDoubleEnumLiteralDeclaration_11()); 
                    // InternalDatatypes.g:722:3: ( 'Double' )
                    // InternalDatatypes.g:722:4: 'Double'
                    {
                    match(input,23,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getDoubleEnumLiteralDeclaration_11()); 

                    }


                    }
                    break;
                case 13 :
                    // InternalDatatypes.g:726:2: ( ( 'ByteBuffer' ) )
                    {
                    // InternalDatatypes.g:726:2: ( ( 'ByteBuffer' ) )
                    // InternalDatatypes.g:727:3: ( 'ByteBuffer' )
                    {
                     before(grammarAccess.getFBasicTypeIdAccess().getByteBufferEnumLiteralDeclaration_12()); 
                    // InternalDatatypes.g:728:3: ( 'ByteBuffer' )
                    // InternalDatatypes.g:728:4: 'ByteBuffer'
                    {
                    match(input,24,FOLLOW_2); 

                    }

                     after(grammarAccess.getFBasicTypeIdAccess().getByteBufferEnumLiteralDeclaration_12()); 

                    }


                    }
                    break;

            }
        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FBasicTypeId__Alternatives"


    // $ANTLR start "rule__Model__Group__0"
    // InternalDatatypes.g:736:1: rule__Model__Group__0 : rule__Model__Group__0__Impl rule__Model__Group__1 ;
    public final void rule__Model__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:740:1: ( rule__Model__Group__0__Impl rule__Model__Group__1 )
            // InternalDatatypes.g:741:2: rule__Model__Group__0__Impl rule__Model__Group__1
            {
            pushFollow(FOLLOW_3);
            rule__Model__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__Model__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__Group__0"


    // $ANTLR start "rule__Model__Group__0__Impl"
    // InternalDatatypes.g:748:1: rule__Model__Group__0__Impl : ( () ) ;
    public final void rule__Model__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:752:1: ( ( () ) )
            // InternalDatatypes.g:753:1: ( () )
            {
            // InternalDatatypes.g:753:1: ( () )
            // InternalDatatypes.g:754:2: ()
            {
             before(grammarAccess.getModelAccess().getModelAction_0()); 
            // InternalDatatypes.g:755:2: ()
            // InternalDatatypes.g:755:3: 
            {
            }

             after(grammarAccess.getModelAccess().getModelAction_0()); 

            }


            }

        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__Group__0__Impl"


    // $ANTLR start "rule__Model__Group__1"
    // InternalDatatypes.g:763:1: rule__Model__Group__1 : rule__Model__Group__1__Impl rule__Model__Group__2 ;
    public final void rule__Model__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:767:1: ( rule__Model__Group__1__Impl rule__Model__Group__2 )
            // InternalDatatypes.g:768:2: rule__Model__Group__1__Impl rule__Model__Group__2
            {
            pushFollow(FOLLOW_4);
            rule__Model__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__Model__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__Group__1"


    // $ANTLR start "rule__Model__Group__1__Impl"
    // InternalDatatypes.g:775:1: rule__Model__Group__1__Impl : ( ( rule__Model__PackAssignment_1 ) ) ;
    public final void rule__Model__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:779:1: ( ( ( rule__Model__PackAssignment_1 ) ) )
            // InternalDatatypes.g:780:1: ( ( rule__Model__PackAssignment_1 ) )
            {
            // InternalDatatypes.g:780:1: ( ( rule__Model__PackAssignment_1 ) )
            // InternalDatatypes.g:781:2: ( rule__Model__PackAssignment_1 )
            {
             before(grammarAccess.getModelAccess().getPackAssignment_1()); 
            // InternalDatatypes.g:782:2: ( rule__Model__PackAssignment_1 )
            // InternalDatatypes.g:782:3: rule__Model__PackAssignment_1
            {
            pushFollow(FOLLOW_2);
            rule__Model__PackAssignment_1();

            state._fsp--;


            }

             after(grammarAccess.getModelAccess().getPackAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__Group__1__Impl"


    // $ANTLR start "rule__Model__Group__2"
    // InternalDatatypes.g:790:1: rule__Model__Group__2 : rule__Model__Group__2__Impl rule__Model__Group__3 ;
    public final void rule__Model__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:794:1: ( rule__Model__Group__2__Impl rule__Model__Group__3 )
            // InternalDatatypes.g:795:2: rule__Model__Group__2__Impl rule__Model__Group__3
            {
            pushFollow(FOLLOW_4);
            rule__Model__Group__2__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__Model__Group__3();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__Group__2"


    // $ANTLR start "rule__Model__Group__2__Impl"
    // InternalDatatypes.g:802:1: rule__Model__Group__2__Impl : ( ( rule__Model__ImportsAssignment_2 )* ) ;
    public final void rule__Model__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:806:1: ( ( ( rule__Model__ImportsAssignment_2 )* ) )
            // InternalDatatypes.g:807:1: ( ( rule__Model__ImportsAssignment_2 )* )
            {
            // InternalDatatypes.g:807:1: ( ( rule__Model__ImportsAssignment_2 )* )
            // InternalDatatypes.g:808:2: ( rule__Model__ImportsAssignment_2 )*
            {
             before(grammarAccess.getModelAccess().getImportsAssignment_2()); 
            // InternalDatatypes.g:809:2: ( rule__Model__ImportsAssignment_2 )*
            loop5:
            do {
                int alt5=2;
                int LA5_0 = input.LA(1);

                if ( (LA5_0==26) ) {
                    alt5=1;
                }


                switch (alt5) {
            	case 1 :
            	    // InternalDatatypes.g:809:3: rule__Model__ImportsAssignment_2
            	    {
            	    pushFollow(FOLLOW_5);
            	    rule__Model__ImportsAssignment_2();

            	    state._fsp--;


            	    }
            	    break;

            	default :
            	    break loop5;
                }
            } while (true);

             after(grammarAccess.getModelAccess().getImportsAssignment_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__Group__2__Impl"


    // $ANTLR start "rule__Model__Group__3"
    // InternalDatatypes.g:817:1: rule__Model__Group__3 : rule__Model__Group__3__Impl ;
    public final void rule__Model__Group__3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:821:1: ( rule__Model__Group__3__Impl )
            // InternalDatatypes.g:822:2: rule__Model__Group__3__Impl
            {
            pushFollow(FOLLOW_2);
            rule__Model__Group__3__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__Group__3"


    // $ANTLR start "rule__Model__Group__3__Impl"
    // InternalDatatypes.g:828:1: rule__Model__Group__3__Impl : ( ( rule__Model__Alternatives_3 )* ) ;
    public final void rule__Model__Group__3__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:832:1: ( ( ( rule__Model__Alternatives_3 )* ) )
            // InternalDatatypes.g:833:1: ( ( rule__Model__Alternatives_3 )* )
            {
            // InternalDatatypes.g:833:1: ( ( rule__Model__Alternatives_3 )* )
            // InternalDatatypes.g:834:2: ( rule__Model__Alternatives_3 )*
            {
             before(grammarAccess.getModelAccess().getAlternatives_3()); 
            // InternalDatatypes.g:835:2: ( rule__Model__Alternatives_3 )*
            loop6:
            do {
                int alt6=2;
                int LA6_0 = input.LA(1);

                if ( (LA6_0==29||LA6_0==31||LA6_0==35) ) {
                    alt6=1;
                }


                switch (alt6) {
            	case 1 :
            	    // InternalDatatypes.g:835:3: rule__Model__Alternatives_3
            	    {
            	    pushFollow(FOLLOW_6);
            	    rule__Model__Alternatives_3();

            	    state._fsp--;


            	    }
            	    break;

            	default :
            	    break loop6;
                }
            } while (true);

             after(grammarAccess.getModelAccess().getAlternatives_3()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__Group__3__Impl"


    // $ANTLR start "rule__Package__Group__0"
    // InternalDatatypes.g:844:1: rule__Package__Group__0 : rule__Package__Group__0__Impl rule__Package__Group__1 ;
    public final void rule__Package__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:848:1: ( rule__Package__Group__0__Impl rule__Package__Group__1 )
            // InternalDatatypes.g:849:2: rule__Package__Group__0__Impl rule__Package__Group__1
            {
            pushFollow(FOLLOW_7);
            rule__Package__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__Package__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Package__Group__0"


    // $ANTLR start "rule__Package__Group__0__Impl"
    // InternalDatatypes.g:856:1: rule__Package__Group__0__Impl : ( 'package' ) ;
    public final void rule__Package__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:860:1: ( ( 'package' ) )
            // InternalDatatypes.g:861:1: ( 'package' )
            {
            // InternalDatatypes.g:861:1: ( 'package' )
            // InternalDatatypes.g:862:2: 'package'
            {
             before(grammarAccess.getPackageAccess().getPackageKeyword_0()); 
            match(input,25,FOLLOW_2); 
             after(grammarAccess.getPackageAccess().getPackageKeyword_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Package__Group__0__Impl"


    // $ANTLR start "rule__Package__Group__1"
    // InternalDatatypes.g:871:1: rule__Package__Group__1 : rule__Package__Group__1__Impl ;
    public final void rule__Package__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:875:1: ( rule__Package__Group__1__Impl )
            // InternalDatatypes.g:876:2: rule__Package__Group__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__Package__Group__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Package__Group__1"


    // $ANTLR start "rule__Package__Group__1__Impl"
    // InternalDatatypes.g:882:1: rule__Package__Group__1__Impl : ( ( rule__Package__NameAssignment_1 ) ) ;
    public final void rule__Package__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:886:1: ( ( ( rule__Package__NameAssignment_1 ) ) )
            // InternalDatatypes.g:887:1: ( ( rule__Package__NameAssignment_1 ) )
            {
            // InternalDatatypes.g:887:1: ( ( rule__Package__NameAssignment_1 ) )
            // InternalDatatypes.g:888:2: ( rule__Package__NameAssignment_1 )
            {
             before(grammarAccess.getPackageAccess().getNameAssignment_1()); 
            // InternalDatatypes.g:889:2: ( rule__Package__NameAssignment_1 )
            // InternalDatatypes.g:889:3: rule__Package__NameAssignment_1
            {
            pushFollow(FOLLOW_2);
            rule__Package__NameAssignment_1();

            state._fsp--;


            }

             after(grammarAccess.getPackageAccess().getNameAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Package__Group__1__Impl"


    // $ANTLR start "rule__Import__Group__0"
    // InternalDatatypes.g:898:1: rule__Import__Group__0 : rule__Import__Group__0__Impl rule__Import__Group__1 ;
    public final void rule__Import__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:902:1: ( rule__Import__Group__0__Impl rule__Import__Group__1 )
            // InternalDatatypes.g:903:2: rule__Import__Group__0__Impl rule__Import__Group__1
            {
            pushFollow(FOLLOW_7);
            rule__Import__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__Import__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Import__Group__0"


    // $ANTLR start "rule__Import__Group__0__Impl"
    // InternalDatatypes.g:910:1: rule__Import__Group__0__Impl : ( 'import' ) ;
    public final void rule__Import__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:914:1: ( ( 'import' ) )
            // InternalDatatypes.g:915:1: ( 'import' )
            {
            // InternalDatatypes.g:915:1: ( 'import' )
            // InternalDatatypes.g:916:2: 'import'
            {
             before(grammarAccess.getImportAccess().getImportKeyword_0()); 
            match(input,26,FOLLOW_2); 
             after(grammarAccess.getImportAccess().getImportKeyword_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Import__Group__0__Impl"


    // $ANTLR start "rule__Import__Group__1"
    // InternalDatatypes.g:925:1: rule__Import__Group__1 : rule__Import__Group__1__Impl ;
    public final void rule__Import__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:929:1: ( rule__Import__Group__1__Impl )
            // InternalDatatypes.g:930:2: rule__Import__Group__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__Import__Group__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Import__Group__1"


    // $ANTLR start "rule__Import__Group__1__Impl"
    // InternalDatatypes.g:936:1: rule__Import__Group__1__Impl : ( ( rule__Import__ImportedNamespaceAssignment_1 ) ) ;
    public final void rule__Import__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:940:1: ( ( ( rule__Import__ImportedNamespaceAssignment_1 ) ) )
            // InternalDatatypes.g:941:1: ( ( rule__Import__ImportedNamespaceAssignment_1 ) )
            {
            // InternalDatatypes.g:941:1: ( ( rule__Import__ImportedNamespaceAssignment_1 ) )
            // InternalDatatypes.g:942:2: ( rule__Import__ImportedNamespaceAssignment_1 )
            {
             before(grammarAccess.getImportAccess().getImportedNamespaceAssignment_1()); 
            // InternalDatatypes.g:943:2: ( rule__Import__ImportedNamespaceAssignment_1 )
            // InternalDatatypes.g:943:3: rule__Import__ImportedNamespaceAssignment_1
            {
            pushFollow(FOLLOW_2);
            rule__Import__ImportedNamespaceAssignment_1();

            state._fsp--;


            }

             after(grammarAccess.getImportAccess().getImportedNamespaceAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Import__Group__1__Impl"


    // $ANTLR start "rule__ImportedFQN__Group__0"
    // InternalDatatypes.g:952:1: rule__ImportedFQN__Group__0 : rule__ImportedFQN__Group__0__Impl rule__ImportedFQN__Group__1 ;
    public final void rule__ImportedFQN__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:956:1: ( rule__ImportedFQN__Group__0__Impl rule__ImportedFQN__Group__1 )
            // InternalDatatypes.g:957:2: rule__ImportedFQN__Group__0__Impl rule__ImportedFQN__Group__1
            {
            pushFollow(FOLLOW_8);
            rule__ImportedFQN__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__ImportedFQN__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__ImportedFQN__Group__0"


    // $ANTLR start "rule__ImportedFQN__Group__0__Impl"
    // InternalDatatypes.g:964:1: rule__ImportedFQN__Group__0__Impl : ( ruleFQN ) ;
    public final void rule__ImportedFQN__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:968:1: ( ( ruleFQN ) )
            // InternalDatatypes.g:969:1: ( ruleFQN )
            {
            // InternalDatatypes.g:969:1: ( ruleFQN )
            // InternalDatatypes.g:970:2: ruleFQN
            {
             before(grammarAccess.getImportedFQNAccess().getFQNParserRuleCall_0()); 
            pushFollow(FOLLOW_2);
            ruleFQN();

            state._fsp--;

             after(grammarAccess.getImportedFQNAccess().getFQNParserRuleCall_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__ImportedFQN__Group__0__Impl"


    // $ANTLR start "rule__ImportedFQN__Group__1"
    // InternalDatatypes.g:979:1: rule__ImportedFQN__Group__1 : rule__ImportedFQN__Group__1__Impl ;
    public final void rule__ImportedFQN__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:983:1: ( rule__ImportedFQN__Group__1__Impl )
            // InternalDatatypes.g:984:2: rule__ImportedFQN__Group__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__ImportedFQN__Group__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__ImportedFQN__Group__1"


    // $ANTLR start "rule__ImportedFQN__Group__1__Impl"
    // InternalDatatypes.g:990:1: rule__ImportedFQN__Group__1__Impl : ( ( rule__ImportedFQN__Group_1__0 )? ) ;
    public final void rule__ImportedFQN__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:994:1: ( ( ( rule__ImportedFQN__Group_1__0 )? ) )
            // InternalDatatypes.g:995:1: ( ( rule__ImportedFQN__Group_1__0 )? )
            {
            // InternalDatatypes.g:995:1: ( ( rule__ImportedFQN__Group_1__0 )? )
            // InternalDatatypes.g:996:2: ( rule__ImportedFQN__Group_1__0 )?
            {
             before(grammarAccess.getImportedFQNAccess().getGroup_1()); 
            // InternalDatatypes.g:997:2: ( rule__ImportedFQN__Group_1__0 )?
            int alt7=2;
            int LA7_0 = input.LA(1);

            if ( (LA7_0==27) ) {
                alt7=1;
            }
            switch (alt7) {
                case 1 :
                    // InternalDatatypes.g:997:3: rule__ImportedFQN__Group_1__0
                    {
                    pushFollow(FOLLOW_2);
                    rule__ImportedFQN__Group_1__0();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getImportedFQNAccess().getGroup_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__ImportedFQN__Group__1__Impl"


    // $ANTLR start "rule__ImportedFQN__Group_1__0"
    // InternalDatatypes.g:1006:1: rule__ImportedFQN__Group_1__0 : rule__ImportedFQN__Group_1__0__Impl rule__ImportedFQN__Group_1__1 ;
    public final void rule__ImportedFQN__Group_1__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1010:1: ( rule__ImportedFQN__Group_1__0__Impl rule__ImportedFQN__Group_1__1 )
            // InternalDatatypes.g:1011:2: rule__ImportedFQN__Group_1__0__Impl rule__ImportedFQN__Group_1__1
            {
            pushFollow(FOLLOW_9);
            rule__ImportedFQN__Group_1__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__ImportedFQN__Group_1__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__ImportedFQN__Group_1__0"


    // $ANTLR start "rule__ImportedFQN__Group_1__0__Impl"
    // InternalDatatypes.g:1018:1: rule__ImportedFQN__Group_1__0__Impl : ( '.' ) ;
    public final void rule__ImportedFQN__Group_1__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1022:1: ( ( '.' ) )
            // InternalDatatypes.g:1023:1: ( '.' )
            {
            // InternalDatatypes.g:1023:1: ( '.' )
            // InternalDatatypes.g:1024:2: '.'
            {
             before(grammarAccess.getImportedFQNAccess().getFullStopKeyword_1_0()); 
            match(input,27,FOLLOW_2); 
             after(grammarAccess.getImportedFQNAccess().getFullStopKeyword_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__ImportedFQN__Group_1__0__Impl"


    // $ANTLR start "rule__ImportedFQN__Group_1__1"
    // InternalDatatypes.g:1033:1: rule__ImportedFQN__Group_1__1 : rule__ImportedFQN__Group_1__1__Impl ;
    public final void rule__ImportedFQN__Group_1__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1037:1: ( rule__ImportedFQN__Group_1__1__Impl )
            // InternalDatatypes.g:1038:2: rule__ImportedFQN__Group_1__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__ImportedFQN__Group_1__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__ImportedFQN__Group_1__1"


    // $ANTLR start "rule__ImportedFQN__Group_1__1__Impl"
    // InternalDatatypes.g:1044:1: rule__ImportedFQN__Group_1__1__Impl : ( '*' ) ;
    public final void rule__ImportedFQN__Group_1__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1048:1: ( ( '*' ) )
            // InternalDatatypes.g:1049:1: ( '*' )
            {
            // InternalDatatypes.g:1049:1: ( '*' )
            // InternalDatatypes.g:1050:2: '*'
            {
             before(grammarAccess.getImportedFQNAccess().getAsteriskKeyword_1_1()); 
            match(input,28,FOLLOW_2); 
             after(grammarAccess.getImportedFQNAccess().getAsteriskKeyword_1_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__ImportedFQN__Group_1__1__Impl"


    // $ANTLR start "rule__FQN__Group__0"
    // InternalDatatypes.g:1060:1: rule__FQN__Group__0 : rule__FQN__Group__0__Impl rule__FQN__Group__1 ;
    public final void rule__FQN__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1064:1: ( rule__FQN__Group__0__Impl rule__FQN__Group__1 )
            // InternalDatatypes.g:1065:2: rule__FQN__Group__0__Impl rule__FQN__Group__1
            {
            pushFollow(FOLLOW_8);
            rule__FQN__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FQN__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FQN__Group__0"


    // $ANTLR start "rule__FQN__Group__0__Impl"
    // InternalDatatypes.g:1072:1: rule__FQN__Group__0__Impl : ( RULE_ID ) ;
    public final void rule__FQN__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1076:1: ( ( RULE_ID ) )
            // InternalDatatypes.g:1077:1: ( RULE_ID )
            {
            // InternalDatatypes.g:1077:1: ( RULE_ID )
            // InternalDatatypes.g:1078:2: RULE_ID
            {
             before(grammarAccess.getFQNAccess().getIDTerminalRuleCall_0()); 
            match(input,RULE_ID,FOLLOW_2); 
             after(grammarAccess.getFQNAccess().getIDTerminalRuleCall_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FQN__Group__0__Impl"


    // $ANTLR start "rule__FQN__Group__1"
    // InternalDatatypes.g:1087:1: rule__FQN__Group__1 : rule__FQN__Group__1__Impl ;
    public final void rule__FQN__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1091:1: ( rule__FQN__Group__1__Impl )
            // InternalDatatypes.g:1092:2: rule__FQN__Group__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FQN__Group__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FQN__Group__1"


    // $ANTLR start "rule__FQN__Group__1__Impl"
    // InternalDatatypes.g:1098:1: rule__FQN__Group__1__Impl : ( ( rule__FQN__Group_1__0 )* ) ;
    public final void rule__FQN__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1102:1: ( ( ( rule__FQN__Group_1__0 )* ) )
            // InternalDatatypes.g:1103:1: ( ( rule__FQN__Group_1__0 )* )
            {
            // InternalDatatypes.g:1103:1: ( ( rule__FQN__Group_1__0 )* )
            // InternalDatatypes.g:1104:2: ( rule__FQN__Group_1__0 )*
            {
             before(grammarAccess.getFQNAccess().getGroup_1()); 
            // InternalDatatypes.g:1105:2: ( rule__FQN__Group_1__0 )*
            loop8:
            do {
                int alt8=2;
                int LA8_0 = input.LA(1);

                if ( (LA8_0==27) ) {
                    int LA8_2 = input.LA(2);

                    if ( (LA8_2==RULE_ID) ) {
                        alt8=1;
                    }


                }


                switch (alt8) {
            	case 1 :
            	    // InternalDatatypes.g:1105:3: rule__FQN__Group_1__0
            	    {
            	    pushFollow(FOLLOW_10);
            	    rule__FQN__Group_1__0();

            	    state._fsp--;


            	    }
            	    break;

            	default :
            	    break loop8;
                }
            } while (true);

             after(grammarAccess.getFQNAccess().getGroup_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FQN__Group__1__Impl"


    // $ANTLR start "rule__FQN__Group_1__0"
    // InternalDatatypes.g:1114:1: rule__FQN__Group_1__0 : rule__FQN__Group_1__0__Impl rule__FQN__Group_1__1 ;
    public final void rule__FQN__Group_1__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1118:1: ( rule__FQN__Group_1__0__Impl rule__FQN__Group_1__1 )
            // InternalDatatypes.g:1119:2: rule__FQN__Group_1__0__Impl rule__FQN__Group_1__1
            {
            pushFollow(FOLLOW_7);
            rule__FQN__Group_1__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FQN__Group_1__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FQN__Group_1__0"


    // $ANTLR start "rule__FQN__Group_1__0__Impl"
    // InternalDatatypes.g:1126:1: rule__FQN__Group_1__0__Impl : ( '.' ) ;
    public final void rule__FQN__Group_1__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1130:1: ( ( '.' ) )
            // InternalDatatypes.g:1131:1: ( '.' )
            {
            // InternalDatatypes.g:1131:1: ( '.' )
            // InternalDatatypes.g:1132:2: '.'
            {
             before(grammarAccess.getFQNAccess().getFullStopKeyword_1_0()); 
            match(input,27,FOLLOW_2); 
             after(grammarAccess.getFQNAccess().getFullStopKeyword_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FQN__Group_1__0__Impl"


    // $ANTLR start "rule__FQN__Group_1__1"
    // InternalDatatypes.g:1141:1: rule__FQN__Group_1__1 : rule__FQN__Group_1__1__Impl ;
    public final void rule__FQN__Group_1__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1145:1: ( rule__FQN__Group_1__1__Impl )
            // InternalDatatypes.g:1146:2: rule__FQN__Group_1__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FQN__Group_1__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FQN__Group_1__1"


    // $ANTLR start "rule__FQN__Group_1__1__Impl"
    // InternalDatatypes.g:1152:1: rule__FQN__Group_1__1__Impl : ( RULE_ID ) ;
    public final void rule__FQN__Group_1__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1156:1: ( ( RULE_ID ) )
            // InternalDatatypes.g:1157:1: ( RULE_ID )
            {
            // InternalDatatypes.g:1157:1: ( RULE_ID )
            // InternalDatatypes.g:1158:2: RULE_ID
            {
             before(grammarAccess.getFQNAccess().getIDTerminalRuleCall_1_1()); 
            match(input,RULE_ID,FOLLOW_2); 
             after(grammarAccess.getFQNAccess().getIDTerminalRuleCall_1_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FQN__Group_1__1__Impl"


    // $ANTLR start "rule__FAnnotationBlock__Group__0"
    // InternalDatatypes.g:1168:1: rule__FAnnotationBlock__Group__0 : rule__FAnnotationBlock__Group__0__Impl rule__FAnnotationBlock__Group__1 ;
    public final void rule__FAnnotationBlock__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1172:1: ( rule__FAnnotationBlock__Group__0__Impl rule__FAnnotationBlock__Group__1 )
            // InternalDatatypes.g:1173:2: rule__FAnnotationBlock__Group__0__Impl rule__FAnnotationBlock__Group__1
            {
            pushFollow(FOLLOW_11);
            rule__FAnnotationBlock__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FAnnotationBlock__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FAnnotationBlock__Group__0"


    // $ANTLR start "rule__FAnnotationBlock__Group__0__Impl"
    // InternalDatatypes.g:1180:1: rule__FAnnotationBlock__Group__0__Impl : ( '<**' ) ;
    public final void rule__FAnnotationBlock__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1184:1: ( ( '<**' ) )
            // InternalDatatypes.g:1185:1: ( '<**' )
            {
            // InternalDatatypes.g:1185:1: ( '<**' )
            // InternalDatatypes.g:1186:2: '<**'
            {
             before(grammarAccess.getFAnnotationBlockAccess().getLessThanSignAsteriskAsteriskKeyword_0()); 
            match(input,29,FOLLOW_2); 
             after(grammarAccess.getFAnnotationBlockAccess().getLessThanSignAsteriskAsteriskKeyword_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FAnnotationBlock__Group__0__Impl"


    // $ANTLR start "rule__FAnnotationBlock__Group__1"
    // InternalDatatypes.g:1195:1: rule__FAnnotationBlock__Group__1 : rule__FAnnotationBlock__Group__1__Impl rule__FAnnotationBlock__Group__2 ;
    public final void rule__FAnnotationBlock__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1199:1: ( rule__FAnnotationBlock__Group__1__Impl rule__FAnnotationBlock__Group__2 )
            // InternalDatatypes.g:1200:2: rule__FAnnotationBlock__Group__1__Impl rule__FAnnotationBlock__Group__2
            {
            pushFollow(FOLLOW_12);
            rule__FAnnotationBlock__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FAnnotationBlock__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FAnnotationBlock__Group__1"


    // $ANTLR start "rule__FAnnotationBlock__Group__1__Impl"
    // InternalDatatypes.g:1207:1: rule__FAnnotationBlock__Group__1__Impl : ( ( ( rule__FAnnotationBlock__ElementsAssignment_1 ) ) ( ( rule__FAnnotationBlock__ElementsAssignment_1 )* ) ) ;
    public final void rule__FAnnotationBlock__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1211:1: ( ( ( ( rule__FAnnotationBlock__ElementsAssignment_1 ) ) ( ( rule__FAnnotationBlock__ElementsAssignment_1 )* ) ) )
            // InternalDatatypes.g:1212:1: ( ( ( rule__FAnnotationBlock__ElementsAssignment_1 ) ) ( ( rule__FAnnotationBlock__ElementsAssignment_1 )* ) )
            {
            // InternalDatatypes.g:1212:1: ( ( ( rule__FAnnotationBlock__ElementsAssignment_1 ) ) ( ( rule__FAnnotationBlock__ElementsAssignment_1 )* ) )
            // InternalDatatypes.g:1213:2: ( ( rule__FAnnotationBlock__ElementsAssignment_1 ) ) ( ( rule__FAnnotationBlock__ElementsAssignment_1 )* )
            {
            // InternalDatatypes.g:1213:2: ( ( rule__FAnnotationBlock__ElementsAssignment_1 ) )
            // InternalDatatypes.g:1214:3: ( rule__FAnnotationBlock__ElementsAssignment_1 )
            {
             before(grammarAccess.getFAnnotationBlockAccess().getElementsAssignment_1()); 
            // InternalDatatypes.g:1215:3: ( rule__FAnnotationBlock__ElementsAssignment_1 )
            // InternalDatatypes.g:1215:4: rule__FAnnotationBlock__ElementsAssignment_1
            {
            pushFollow(FOLLOW_13);
            rule__FAnnotationBlock__ElementsAssignment_1();

            state._fsp--;


            }

             after(grammarAccess.getFAnnotationBlockAccess().getElementsAssignment_1()); 

            }

            // InternalDatatypes.g:1218:2: ( ( rule__FAnnotationBlock__ElementsAssignment_1 )* )
            // InternalDatatypes.g:1219:3: ( rule__FAnnotationBlock__ElementsAssignment_1 )*
            {
             before(grammarAccess.getFAnnotationBlockAccess().getElementsAssignment_1()); 
            // InternalDatatypes.g:1220:3: ( rule__FAnnotationBlock__ElementsAssignment_1 )*
            loop9:
            do {
                int alt9=2;
                int LA9_0 = input.LA(1);

                if ( (LA9_0==RULE_ANNOTATION_STRING) ) {
                    alt9=1;
                }


                switch (alt9) {
            	case 1 :
            	    // InternalDatatypes.g:1220:4: rule__FAnnotationBlock__ElementsAssignment_1
            	    {
            	    pushFollow(FOLLOW_13);
            	    rule__FAnnotationBlock__ElementsAssignment_1();

            	    state._fsp--;


            	    }
            	    break;

            	default :
            	    break loop9;
                }
            } while (true);

             after(grammarAccess.getFAnnotationBlockAccess().getElementsAssignment_1()); 

            }


            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FAnnotationBlock__Group__1__Impl"


    // $ANTLR start "rule__FAnnotationBlock__Group__2"
    // InternalDatatypes.g:1229:1: rule__FAnnotationBlock__Group__2 : rule__FAnnotationBlock__Group__2__Impl ;
    public final void rule__FAnnotationBlock__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1233:1: ( rule__FAnnotationBlock__Group__2__Impl )
            // InternalDatatypes.g:1234:2: rule__FAnnotationBlock__Group__2__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FAnnotationBlock__Group__2__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FAnnotationBlock__Group__2"


    // $ANTLR start "rule__FAnnotationBlock__Group__2__Impl"
    // InternalDatatypes.g:1240:1: rule__FAnnotationBlock__Group__2__Impl : ( '**>' ) ;
    public final void rule__FAnnotationBlock__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1244:1: ( ( '**>' ) )
            // InternalDatatypes.g:1245:1: ( '**>' )
            {
            // InternalDatatypes.g:1245:1: ( '**>' )
            // InternalDatatypes.g:1246:2: '**>'
            {
             before(grammarAccess.getFAnnotationBlockAccess().getAsteriskAsteriskGreaterThanSignKeyword_2()); 
            match(input,30,FOLLOW_2); 
             after(grammarAccess.getFAnnotationBlockAccess().getAsteriskAsteriskGreaterThanSignKeyword_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FAnnotationBlock__Group__2__Impl"


    // $ANTLR start "rule__FTypeCollection__Group__0"
    // InternalDatatypes.g:1256:1: rule__FTypeCollection__Group__0 : rule__FTypeCollection__Group__0__Impl rule__FTypeCollection__Group__1 ;
    public final void rule__FTypeCollection__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1260:1: ( rule__FTypeCollection__Group__0__Impl rule__FTypeCollection__Group__1 )
            // InternalDatatypes.g:1261:2: rule__FTypeCollection__Group__0__Impl rule__FTypeCollection__Group__1
            {
            pushFollow(FOLLOW_14);
            rule__FTypeCollection__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeCollection__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__0"


    // $ANTLR start "rule__FTypeCollection__Group__0__Impl"
    // InternalDatatypes.g:1268:1: rule__FTypeCollection__Group__0__Impl : ( () ) ;
    public final void rule__FTypeCollection__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1272:1: ( ( () ) )
            // InternalDatatypes.g:1273:1: ( () )
            {
            // InternalDatatypes.g:1273:1: ( () )
            // InternalDatatypes.g:1274:2: ()
            {
             before(grammarAccess.getFTypeCollectionAccess().getFTypeCollectionAction_0()); 
            // InternalDatatypes.g:1275:2: ()
            // InternalDatatypes.g:1275:3: 
            {
            }

             after(grammarAccess.getFTypeCollectionAccess().getFTypeCollectionAction_0()); 

            }


            }

        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__0__Impl"


    // $ANTLR start "rule__FTypeCollection__Group__1"
    // InternalDatatypes.g:1283:1: rule__FTypeCollection__Group__1 : rule__FTypeCollection__Group__1__Impl rule__FTypeCollection__Group__2 ;
    public final void rule__FTypeCollection__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1287:1: ( rule__FTypeCollection__Group__1__Impl rule__FTypeCollection__Group__2 )
            // InternalDatatypes.g:1288:2: rule__FTypeCollection__Group__1__Impl rule__FTypeCollection__Group__2
            {
            pushFollow(FOLLOW_14);
            rule__FTypeCollection__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeCollection__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__1"


    // $ANTLR start "rule__FTypeCollection__Group__1__Impl"
    // InternalDatatypes.g:1295:1: rule__FTypeCollection__Group__1__Impl : ( ( rule__FTypeCollection__CommentAssignment_1 )? ) ;
    public final void rule__FTypeCollection__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1299:1: ( ( ( rule__FTypeCollection__CommentAssignment_1 )? ) )
            // InternalDatatypes.g:1300:1: ( ( rule__FTypeCollection__CommentAssignment_1 )? )
            {
            // InternalDatatypes.g:1300:1: ( ( rule__FTypeCollection__CommentAssignment_1 )? )
            // InternalDatatypes.g:1301:2: ( rule__FTypeCollection__CommentAssignment_1 )?
            {
             before(grammarAccess.getFTypeCollectionAccess().getCommentAssignment_1()); 
            // InternalDatatypes.g:1302:2: ( rule__FTypeCollection__CommentAssignment_1 )?
            int alt10=2;
            int LA10_0 = input.LA(1);

            if ( (LA10_0==29) ) {
                alt10=1;
            }
            switch (alt10) {
                case 1 :
                    // InternalDatatypes.g:1302:3: rule__FTypeCollection__CommentAssignment_1
                    {
                    pushFollow(FOLLOW_2);
                    rule__FTypeCollection__CommentAssignment_1();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFTypeCollectionAccess().getCommentAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__1__Impl"


    // $ANTLR start "rule__FTypeCollection__Group__2"
    // InternalDatatypes.g:1310:1: rule__FTypeCollection__Group__2 : rule__FTypeCollection__Group__2__Impl rule__FTypeCollection__Group__3 ;
    public final void rule__FTypeCollection__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1314:1: ( rule__FTypeCollection__Group__2__Impl rule__FTypeCollection__Group__3 )
            // InternalDatatypes.g:1315:2: rule__FTypeCollection__Group__2__Impl rule__FTypeCollection__Group__3
            {
            pushFollow(FOLLOW_15);
            rule__FTypeCollection__Group__2__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeCollection__Group__3();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__2"


    // $ANTLR start "rule__FTypeCollection__Group__2__Impl"
    // InternalDatatypes.g:1322:1: rule__FTypeCollection__Group__2__Impl : ( 'typeCollection' ) ;
    public final void rule__FTypeCollection__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1326:1: ( ( 'typeCollection' ) )
            // InternalDatatypes.g:1327:1: ( 'typeCollection' )
            {
            // InternalDatatypes.g:1327:1: ( 'typeCollection' )
            // InternalDatatypes.g:1328:2: 'typeCollection'
            {
             before(grammarAccess.getFTypeCollectionAccess().getTypeCollectionKeyword_2()); 
            match(input,31,FOLLOW_2); 
             after(grammarAccess.getFTypeCollectionAccess().getTypeCollectionKeyword_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__2__Impl"


    // $ANTLR start "rule__FTypeCollection__Group__3"
    // InternalDatatypes.g:1337:1: rule__FTypeCollection__Group__3 : rule__FTypeCollection__Group__3__Impl rule__FTypeCollection__Group__4 ;
    public final void rule__FTypeCollection__Group__3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1341:1: ( rule__FTypeCollection__Group__3__Impl rule__FTypeCollection__Group__4 )
            // InternalDatatypes.g:1342:2: rule__FTypeCollection__Group__3__Impl rule__FTypeCollection__Group__4
            {
            pushFollow(FOLLOW_15);
            rule__FTypeCollection__Group__3__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeCollection__Group__4();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__3"


    // $ANTLR start "rule__FTypeCollection__Group__3__Impl"
    // InternalDatatypes.g:1349:1: rule__FTypeCollection__Group__3__Impl : ( ( rule__FTypeCollection__NameAssignment_3 )? ) ;
    public final void rule__FTypeCollection__Group__3__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1353:1: ( ( ( rule__FTypeCollection__NameAssignment_3 )? ) )
            // InternalDatatypes.g:1354:1: ( ( rule__FTypeCollection__NameAssignment_3 )? )
            {
            // InternalDatatypes.g:1354:1: ( ( rule__FTypeCollection__NameAssignment_3 )? )
            // InternalDatatypes.g:1355:2: ( rule__FTypeCollection__NameAssignment_3 )?
            {
             before(grammarAccess.getFTypeCollectionAccess().getNameAssignment_3()); 
            // InternalDatatypes.g:1356:2: ( rule__FTypeCollection__NameAssignment_3 )?
            int alt11=2;
            int LA11_0 = input.LA(1);

            if ( (LA11_0==RULE_ID) ) {
                alt11=1;
            }
            switch (alt11) {
                case 1 :
                    // InternalDatatypes.g:1356:3: rule__FTypeCollection__NameAssignment_3
                    {
                    pushFollow(FOLLOW_2);
                    rule__FTypeCollection__NameAssignment_3();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFTypeCollectionAccess().getNameAssignment_3()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__3__Impl"


    // $ANTLR start "rule__FTypeCollection__Group__4"
    // InternalDatatypes.g:1364:1: rule__FTypeCollection__Group__4 : rule__FTypeCollection__Group__4__Impl rule__FTypeCollection__Group__5 ;
    public final void rule__FTypeCollection__Group__4() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1368:1: ( rule__FTypeCollection__Group__4__Impl rule__FTypeCollection__Group__5 )
            // InternalDatatypes.g:1369:2: rule__FTypeCollection__Group__4__Impl rule__FTypeCollection__Group__5
            {
            pushFollow(FOLLOW_16);
            rule__FTypeCollection__Group__4__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeCollection__Group__5();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__4"


    // $ANTLR start "rule__FTypeCollection__Group__4__Impl"
    // InternalDatatypes.g:1376:1: rule__FTypeCollection__Group__4__Impl : ( '{' ) ;
    public final void rule__FTypeCollection__Group__4__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1380:1: ( ( '{' ) )
            // InternalDatatypes.g:1381:1: ( '{' )
            {
            // InternalDatatypes.g:1381:1: ( '{' )
            // InternalDatatypes.g:1382:2: '{'
            {
             before(grammarAccess.getFTypeCollectionAccess().getLeftCurlyBracketKeyword_4()); 
            match(input,32,FOLLOW_2); 
             after(grammarAccess.getFTypeCollectionAccess().getLeftCurlyBracketKeyword_4()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__4__Impl"


    // $ANTLR start "rule__FTypeCollection__Group__5"
    // InternalDatatypes.g:1391:1: rule__FTypeCollection__Group__5 : rule__FTypeCollection__Group__5__Impl rule__FTypeCollection__Group__6 ;
    public final void rule__FTypeCollection__Group__5() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1395:1: ( rule__FTypeCollection__Group__5__Impl rule__FTypeCollection__Group__6 )
            // InternalDatatypes.g:1396:2: rule__FTypeCollection__Group__5__Impl rule__FTypeCollection__Group__6
            {
            pushFollow(FOLLOW_16);
            rule__FTypeCollection__Group__5__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeCollection__Group__6();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__5"


    // $ANTLR start "rule__FTypeCollection__Group__5__Impl"
    // InternalDatatypes.g:1403:1: rule__FTypeCollection__Group__5__Impl : ( ( rule__FTypeCollection__Group_5__0 )? ) ;
    public final void rule__FTypeCollection__Group__5__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1407:1: ( ( ( rule__FTypeCollection__Group_5__0 )? ) )
            // InternalDatatypes.g:1408:1: ( ( rule__FTypeCollection__Group_5__0 )? )
            {
            // InternalDatatypes.g:1408:1: ( ( rule__FTypeCollection__Group_5__0 )? )
            // InternalDatatypes.g:1409:2: ( rule__FTypeCollection__Group_5__0 )?
            {
             before(grammarAccess.getFTypeCollectionAccess().getGroup_5()); 
            // InternalDatatypes.g:1410:2: ( rule__FTypeCollection__Group_5__0 )?
            int alt12=2;
            int LA12_0 = input.LA(1);

            if ( (LA12_0==34) ) {
                alt12=1;
            }
            switch (alt12) {
                case 1 :
                    // InternalDatatypes.g:1410:3: rule__FTypeCollection__Group_5__0
                    {
                    pushFollow(FOLLOW_2);
                    rule__FTypeCollection__Group_5__0();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFTypeCollectionAccess().getGroup_5()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__5__Impl"


    // $ANTLR start "rule__FTypeCollection__Group__6"
    // InternalDatatypes.g:1418:1: rule__FTypeCollection__Group__6 : rule__FTypeCollection__Group__6__Impl rule__FTypeCollection__Group__7 ;
    public final void rule__FTypeCollection__Group__6() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1422:1: ( rule__FTypeCollection__Group__6__Impl rule__FTypeCollection__Group__7 )
            // InternalDatatypes.g:1423:2: rule__FTypeCollection__Group__6__Impl rule__FTypeCollection__Group__7
            {
            pushFollow(FOLLOW_16);
            rule__FTypeCollection__Group__6__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeCollection__Group__7();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__6"


    // $ANTLR start "rule__FTypeCollection__Group__6__Impl"
    // InternalDatatypes.g:1430:1: rule__FTypeCollection__Group__6__Impl : ( ( rule__FTypeCollection__TypesAssignment_6 )* ) ;
    public final void rule__FTypeCollection__Group__6__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1434:1: ( ( ( rule__FTypeCollection__TypesAssignment_6 )* ) )
            // InternalDatatypes.g:1435:1: ( ( rule__FTypeCollection__TypesAssignment_6 )* )
            {
            // InternalDatatypes.g:1435:1: ( ( rule__FTypeCollection__TypesAssignment_6 )* )
            // InternalDatatypes.g:1436:2: ( rule__FTypeCollection__TypesAssignment_6 )*
            {
             before(grammarAccess.getFTypeCollectionAccess().getTypesAssignment_6()); 
            // InternalDatatypes.g:1437:2: ( rule__FTypeCollection__TypesAssignment_6 )*
            loop13:
            do {
                int alt13=2;
                int LA13_0 = input.LA(1);

                if ( (LA13_0==29||LA13_0==39||LA13_0==41||LA13_0==43||LA13_0==45||LA13_0==48) ) {
                    alt13=1;
                }


                switch (alt13) {
            	case 1 :
            	    // InternalDatatypes.g:1437:3: rule__FTypeCollection__TypesAssignment_6
            	    {
            	    pushFollow(FOLLOW_17);
            	    rule__FTypeCollection__TypesAssignment_6();

            	    state._fsp--;


            	    }
            	    break;

            	default :
            	    break loop13;
                }
            } while (true);

             after(grammarAccess.getFTypeCollectionAccess().getTypesAssignment_6()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__6__Impl"


    // $ANTLR start "rule__FTypeCollection__Group__7"
    // InternalDatatypes.g:1445:1: rule__FTypeCollection__Group__7 : rule__FTypeCollection__Group__7__Impl ;
    public final void rule__FTypeCollection__Group__7() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1449:1: ( rule__FTypeCollection__Group__7__Impl )
            // InternalDatatypes.g:1450:2: rule__FTypeCollection__Group__7__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FTypeCollection__Group__7__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__7"


    // $ANTLR start "rule__FTypeCollection__Group__7__Impl"
    // InternalDatatypes.g:1456:1: rule__FTypeCollection__Group__7__Impl : ( '}' ) ;
    public final void rule__FTypeCollection__Group__7__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1460:1: ( ( '}' ) )
            // InternalDatatypes.g:1461:1: ( '}' )
            {
            // InternalDatatypes.g:1461:1: ( '}' )
            // InternalDatatypes.g:1462:2: '}'
            {
             before(grammarAccess.getFTypeCollectionAccess().getRightCurlyBracketKeyword_7()); 
            match(input,33,FOLLOW_2); 
             after(grammarAccess.getFTypeCollectionAccess().getRightCurlyBracketKeyword_7()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group__7__Impl"


    // $ANTLR start "rule__FTypeCollection__Group_5__0"
    // InternalDatatypes.g:1472:1: rule__FTypeCollection__Group_5__0 : rule__FTypeCollection__Group_5__0__Impl rule__FTypeCollection__Group_5__1 ;
    public final void rule__FTypeCollection__Group_5__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1476:1: ( rule__FTypeCollection__Group_5__0__Impl rule__FTypeCollection__Group_5__1 )
            // InternalDatatypes.g:1477:2: rule__FTypeCollection__Group_5__0__Impl rule__FTypeCollection__Group_5__1
            {
            pushFollow(FOLLOW_18);
            rule__FTypeCollection__Group_5__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeCollection__Group_5__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group_5__0"


    // $ANTLR start "rule__FTypeCollection__Group_5__0__Impl"
    // InternalDatatypes.g:1484:1: rule__FTypeCollection__Group_5__0__Impl : ( 'version' ) ;
    public final void rule__FTypeCollection__Group_5__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1488:1: ( ( 'version' ) )
            // InternalDatatypes.g:1489:1: ( 'version' )
            {
            // InternalDatatypes.g:1489:1: ( 'version' )
            // InternalDatatypes.g:1490:2: 'version'
            {
             before(grammarAccess.getFTypeCollectionAccess().getVersionKeyword_5_0()); 
            match(input,34,FOLLOW_2); 
             after(grammarAccess.getFTypeCollectionAccess().getVersionKeyword_5_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group_5__0__Impl"


    // $ANTLR start "rule__FTypeCollection__Group_5__1"
    // InternalDatatypes.g:1499:1: rule__FTypeCollection__Group_5__1 : rule__FTypeCollection__Group_5__1__Impl ;
    public final void rule__FTypeCollection__Group_5__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1503:1: ( rule__FTypeCollection__Group_5__1__Impl )
            // InternalDatatypes.g:1504:2: rule__FTypeCollection__Group_5__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FTypeCollection__Group_5__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group_5__1"


    // $ANTLR start "rule__FTypeCollection__Group_5__1__Impl"
    // InternalDatatypes.g:1510:1: rule__FTypeCollection__Group_5__1__Impl : ( ( rule__FTypeCollection__VersionAssignment_5_1 ) ) ;
    public final void rule__FTypeCollection__Group_5__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1514:1: ( ( ( rule__FTypeCollection__VersionAssignment_5_1 ) ) )
            // InternalDatatypes.g:1515:1: ( ( rule__FTypeCollection__VersionAssignment_5_1 ) )
            {
            // InternalDatatypes.g:1515:1: ( ( rule__FTypeCollection__VersionAssignment_5_1 ) )
            // InternalDatatypes.g:1516:2: ( rule__FTypeCollection__VersionAssignment_5_1 )
            {
             before(grammarAccess.getFTypeCollectionAccess().getVersionAssignment_5_1()); 
            // InternalDatatypes.g:1517:2: ( rule__FTypeCollection__VersionAssignment_5_1 )
            // InternalDatatypes.g:1517:3: rule__FTypeCollection__VersionAssignment_5_1
            {
            pushFollow(FOLLOW_2);
            rule__FTypeCollection__VersionAssignment_5_1();

            state._fsp--;


            }

             after(grammarAccess.getFTypeCollectionAccess().getVersionAssignment_5_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__Group_5__1__Impl"


    // $ANTLR start "rule__FMessageCollection__Group__0"
    // InternalDatatypes.g:1526:1: rule__FMessageCollection__Group__0 : rule__FMessageCollection__Group__0__Impl rule__FMessageCollection__Group__1 ;
    public final void rule__FMessageCollection__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1530:1: ( rule__FMessageCollection__Group__0__Impl rule__FMessageCollection__Group__1 )
            // InternalDatatypes.g:1531:2: rule__FMessageCollection__Group__0__Impl rule__FMessageCollection__Group__1
            {
            pushFollow(FOLLOW_19);
            rule__FMessageCollection__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMessageCollection__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__0"


    // $ANTLR start "rule__FMessageCollection__Group__0__Impl"
    // InternalDatatypes.g:1538:1: rule__FMessageCollection__Group__0__Impl : ( () ) ;
    public final void rule__FMessageCollection__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1542:1: ( ( () ) )
            // InternalDatatypes.g:1543:1: ( () )
            {
            // InternalDatatypes.g:1543:1: ( () )
            // InternalDatatypes.g:1544:2: ()
            {
             before(grammarAccess.getFMessageCollectionAccess().getFMessageCollectionAction_0()); 
            // InternalDatatypes.g:1545:2: ()
            // InternalDatatypes.g:1545:3: 
            {
            }

             after(grammarAccess.getFMessageCollectionAccess().getFMessageCollectionAction_0()); 

            }


            }

        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__0__Impl"


    // $ANTLR start "rule__FMessageCollection__Group__1"
    // InternalDatatypes.g:1553:1: rule__FMessageCollection__Group__1 : rule__FMessageCollection__Group__1__Impl rule__FMessageCollection__Group__2 ;
    public final void rule__FMessageCollection__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1557:1: ( rule__FMessageCollection__Group__1__Impl rule__FMessageCollection__Group__2 )
            // InternalDatatypes.g:1558:2: rule__FMessageCollection__Group__1__Impl rule__FMessageCollection__Group__2
            {
            pushFollow(FOLLOW_19);
            rule__FMessageCollection__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMessageCollection__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__1"


    // $ANTLR start "rule__FMessageCollection__Group__1__Impl"
    // InternalDatatypes.g:1565:1: rule__FMessageCollection__Group__1__Impl : ( ( rule__FMessageCollection__CommentAssignment_1 )? ) ;
    public final void rule__FMessageCollection__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1569:1: ( ( ( rule__FMessageCollection__CommentAssignment_1 )? ) )
            // InternalDatatypes.g:1570:1: ( ( rule__FMessageCollection__CommentAssignment_1 )? )
            {
            // InternalDatatypes.g:1570:1: ( ( rule__FMessageCollection__CommentAssignment_1 )? )
            // InternalDatatypes.g:1571:2: ( rule__FMessageCollection__CommentAssignment_1 )?
            {
             before(grammarAccess.getFMessageCollectionAccess().getCommentAssignment_1()); 
            // InternalDatatypes.g:1572:2: ( rule__FMessageCollection__CommentAssignment_1 )?
            int alt14=2;
            int LA14_0 = input.LA(1);

            if ( (LA14_0==29) ) {
                alt14=1;
            }
            switch (alt14) {
                case 1 :
                    // InternalDatatypes.g:1572:3: rule__FMessageCollection__CommentAssignment_1
                    {
                    pushFollow(FOLLOW_2);
                    rule__FMessageCollection__CommentAssignment_1();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFMessageCollectionAccess().getCommentAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__1__Impl"


    // $ANTLR start "rule__FMessageCollection__Group__2"
    // InternalDatatypes.g:1580:1: rule__FMessageCollection__Group__2 : rule__FMessageCollection__Group__2__Impl rule__FMessageCollection__Group__3 ;
    public final void rule__FMessageCollection__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1584:1: ( rule__FMessageCollection__Group__2__Impl rule__FMessageCollection__Group__3 )
            // InternalDatatypes.g:1585:2: rule__FMessageCollection__Group__2__Impl rule__FMessageCollection__Group__3
            {
            pushFollow(FOLLOW_15);
            rule__FMessageCollection__Group__2__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMessageCollection__Group__3();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__2"


    // $ANTLR start "rule__FMessageCollection__Group__2__Impl"
    // InternalDatatypes.g:1592:1: rule__FMessageCollection__Group__2__Impl : ( 'messageCollection' ) ;
    public final void rule__FMessageCollection__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1596:1: ( ( 'messageCollection' ) )
            // InternalDatatypes.g:1597:1: ( 'messageCollection' )
            {
            // InternalDatatypes.g:1597:1: ( 'messageCollection' )
            // InternalDatatypes.g:1598:2: 'messageCollection'
            {
             before(grammarAccess.getFMessageCollectionAccess().getMessageCollectionKeyword_2()); 
            match(input,35,FOLLOW_2); 
             after(grammarAccess.getFMessageCollectionAccess().getMessageCollectionKeyword_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__2__Impl"


    // $ANTLR start "rule__FMessageCollection__Group__3"
    // InternalDatatypes.g:1607:1: rule__FMessageCollection__Group__3 : rule__FMessageCollection__Group__3__Impl rule__FMessageCollection__Group__4 ;
    public final void rule__FMessageCollection__Group__3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1611:1: ( rule__FMessageCollection__Group__3__Impl rule__FMessageCollection__Group__4 )
            // InternalDatatypes.g:1612:2: rule__FMessageCollection__Group__3__Impl rule__FMessageCollection__Group__4
            {
            pushFollow(FOLLOW_15);
            rule__FMessageCollection__Group__3__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMessageCollection__Group__4();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__3"


    // $ANTLR start "rule__FMessageCollection__Group__3__Impl"
    // InternalDatatypes.g:1619:1: rule__FMessageCollection__Group__3__Impl : ( ( rule__FMessageCollection__NameAssignment_3 )? ) ;
    public final void rule__FMessageCollection__Group__3__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1623:1: ( ( ( rule__FMessageCollection__NameAssignment_3 )? ) )
            // InternalDatatypes.g:1624:1: ( ( rule__FMessageCollection__NameAssignment_3 )? )
            {
            // InternalDatatypes.g:1624:1: ( ( rule__FMessageCollection__NameAssignment_3 )? )
            // InternalDatatypes.g:1625:2: ( rule__FMessageCollection__NameAssignment_3 )?
            {
             before(grammarAccess.getFMessageCollectionAccess().getNameAssignment_3()); 
            // InternalDatatypes.g:1626:2: ( rule__FMessageCollection__NameAssignment_3 )?
            int alt15=2;
            int LA15_0 = input.LA(1);

            if ( (LA15_0==RULE_ID) ) {
                alt15=1;
            }
            switch (alt15) {
                case 1 :
                    // InternalDatatypes.g:1626:3: rule__FMessageCollection__NameAssignment_3
                    {
                    pushFollow(FOLLOW_2);
                    rule__FMessageCollection__NameAssignment_3();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFMessageCollectionAccess().getNameAssignment_3()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__3__Impl"


    // $ANTLR start "rule__FMessageCollection__Group__4"
    // InternalDatatypes.g:1634:1: rule__FMessageCollection__Group__4 : rule__FMessageCollection__Group__4__Impl rule__FMessageCollection__Group__5 ;
    public final void rule__FMessageCollection__Group__4() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1638:1: ( rule__FMessageCollection__Group__4__Impl rule__FMessageCollection__Group__5 )
            // InternalDatatypes.g:1639:2: rule__FMessageCollection__Group__4__Impl rule__FMessageCollection__Group__5
            {
            pushFollow(FOLLOW_20);
            rule__FMessageCollection__Group__4__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMessageCollection__Group__5();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__4"


    // $ANTLR start "rule__FMessageCollection__Group__4__Impl"
    // InternalDatatypes.g:1646:1: rule__FMessageCollection__Group__4__Impl : ( '{' ) ;
    public final void rule__FMessageCollection__Group__4__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1650:1: ( ( '{' ) )
            // InternalDatatypes.g:1651:1: ( '{' )
            {
            // InternalDatatypes.g:1651:1: ( '{' )
            // InternalDatatypes.g:1652:2: '{'
            {
             before(grammarAccess.getFMessageCollectionAccess().getLeftCurlyBracketKeyword_4()); 
            match(input,32,FOLLOW_2); 
             after(grammarAccess.getFMessageCollectionAccess().getLeftCurlyBracketKeyword_4()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__4__Impl"


    // $ANTLR start "rule__FMessageCollection__Group__5"
    // InternalDatatypes.g:1661:1: rule__FMessageCollection__Group__5 : rule__FMessageCollection__Group__5__Impl rule__FMessageCollection__Group__6 ;
    public final void rule__FMessageCollection__Group__5() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1665:1: ( rule__FMessageCollection__Group__5__Impl rule__FMessageCollection__Group__6 )
            // InternalDatatypes.g:1666:2: rule__FMessageCollection__Group__5__Impl rule__FMessageCollection__Group__6
            {
            pushFollow(FOLLOW_20);
            rule__FMessageCollection__Group__5__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMessageCollection__Group__6();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__5"


    // $ANTLR start "rule__FMessageCollection__Group__5__Impl"
    // InternalDatatypes.g:1673:1: rule__FMessageCollection__Group__5__Impl : ( ( rule__FMessageCollection__Group_5__0 )? ) ;
    public final void rule__FMessageCollection__Group__5__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1677:1: ( ( ( rule__FMessageCollection__Group_5__0 )? ) )
            // InternalDatatypes.g:1678:1: ( ( rule__FMessageCollection__Group_5__0 )? )
            {
            // InternalDatatypes.g:1678:1: ( ( rule__FMessageCollection__Group_5__0 )? )
            // InternalDatatypes.g:1679:2: ( rule__FMessageCollection__Group_5__0 )?
            {
             before(grammarAccess.getFMessageCollectionAccess().getGroup_5()); 
            // InternalDatatypes.g:1680:2: ( rule__FMessageCollection__Group_5__0 )?
            int alt16=2;
            int LA16_0 = input.LA(1);

            if ( (LA16_0==34) ) {
                alt16=1;
            }
            switch (alt16) {
                case 1 :
                    // InternalDatatypes.g:1680:3: rule__FMessageCollection__Group_5__0
                    {
                    pushFollow(FOLLOW_2);
                    rule__FMessageCollection__Group_5__0();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFMessageCollectionAccess().getGroup_5()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__5__Impl"


    // $ANTLR start "rule__FMessageCollection__Group__6"
    // InternalDatatypes.g:1688:1: rule__FMessageCollection__Group__6 : rule__FMessageCollection__Group__6__Impl rule__FMessageCollection__Group__7 ;
    public final void rule__FMessageCollection__Group__6() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1692:1: ( rule__FMessageCollection__Group__6__Impl rule__FMessageCollection__Group__7 )
            // InternalDatatypes.g:1693:2: rule__FMessageCollection__Group__6__Impl rule__FMessageCollection__Group__7
            {
            pushFollow(FOLLOW_20);
            rule__FMessageCollection__Group__6__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMessageCollection__Group__7();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__6"


    // $ANTLR start "rule__FMessageCollection__Group__6__Impl"
    // InternalDatatypes.g:1700:1: rule__FMessageCollection__Group__6__Impl : ( ( rule__FMessageCollection__MessagesAssignment_6 )* ) ;
    public final void rule__FMessageCollection__Group__6__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1704:1: ( ( ( rule__FMessageCollection__MessagesAssignment_6 )* ) )
            // InternalDatatypes.g:1705:1: ( ( rule__FMessageCollection__MessagesAssignment_6 )* )
            {
            // InternalDatatypes.g:1705:1: ( ( rule__FMessageCollection__MessagesAssignment_6 )* )
            // InternalDatatypes.g:1706:2: ( rule__FMessageCollection__MessagesAssignment_6 )*
            {
             before(grammarAccess.getFMessageCollectionAccess().getMessagesAssignment_6()); 
            // InternalDatatypes.g:1707:2: ( rule__FMessageCollection__MessagesAssignment_6 )*
            loop17:
            do {
                int alt17=2;
                int LA17_0 = input.LA(1);

                if ( (LA17_0==RULE_ID) ) {
                    alt17=1;
                }


                switch (alt17) {
            	case 1 :
            	    // InternalDatatypes.g:1707:3: rule__FMessageCollection__MessagesAssignment_6
            	    {
            	    pushFollow(FOLLOW_21);
            	    rule__FMessageCollection__MessagesAssignment_6();

            	    state._fsp--;


            	    }
            	    break;

            	default :
            	    break loop17;
                }
            } while (true);

             after(grammarAccess.getFMessageCollectionAccess().getMessagesAssignment_6()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__6__Impl"


    // $ANTLR start "rule__FMessageCollection__Group__7"
    // InternalDatatypes.g:1715:1: rule__FMessageCollection__Group__7 : rule__FMessageCollection__Group__7__Impl ;
    public final void rule__FMessageCollection__Group__7() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1719:1: ( rule__FMessageCollection__Group__7__Impl )
            // InternalDatatypes.g:1720:2: rule__FMessageCollection__Group__7__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FMessageCollection__Group__7__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__7"


    // $ANTLR start "rule__FMessageCollection__Group__7__Impl"
    // InternalDatatypes.g:1726:1: rule__FMessageCollection__Group__7__Impl : ( '}' ) ;
    public final void rule__FMessageCollection__Group__7__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1730:1: ( ( '}' ) )
            // InternalDatatypes.g:1731:1: ( '}' )
            {
            // InternalDatatypes.g:1731:1: ( '}' )
            // InternalDatatypes.g:1732:2: '}'
            {
             before(grammarAccess.getFMessageCollectionAccess().getRightCurlyBracketKeyword_7()); 
            match(input,33,FOLLOW_2); 
             after(grammarAccess.getFMessageCollectionAccess().getRightCurlyBracketKeyword_7()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group__7__Impl"


    // $ANTLR start "rule__FMessageCollection__Group_5__0"
    // InternalDatatypes.g:1742:1: rule__FMessageCollection__Group_5__0 : rule__FMessageCollection__Group_5__0__Impl rule__FMessageCollection__Group_5__1 ;
    public final void rule__FMessageCollection__Group_5__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1746:1: ( rule__FMessageCollection__Group_5__0__Impl rule__FMessageCollection__Group_5__1 )
            // InternalDatatypes.g:1747:2: rule__FMessageCollection__Group_5__0__Impl rule__FMessageCollection__Group_5__1
            {
            pushFollow(FOLLOW_18);
            rule__FMessageCollection__Group_5__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMessageCollection__Group_5__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group_5__0"


    // $ANTLR start "rule__FMessageCollection__Group_5__0__Impl"
    // InternalDatatypes.g:1754:1: rule__FMessageCollection__Group_5__0__Impl : ( 'version' ) ;
    public final void rule__FMessageCollection__Group_5__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1758:1: ( ( 'version' ) )
            // InternalDatatypes.g:1759:1: ( 'version' )
            {
            // InternalDatatypes.g:1759:1: ( 'version' )
            // InternalDatatypes.g:1760:2: 'version'
            {
             before(grammarAccess.getFMessageCollectionAccess().getVersionKeyword_5_0()); 
            match(input,34,FOLLOW_2); 
             after(grammarAccess.getFMessageCollectionAccess().getVersionKeyword_5_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group_5__0__Impl"


    // $ANTLR start "rule__FMessageCollection__Group_5__1"
    // InternalDatatypes.g:1769:1: rule__FMessageCollection__Group_5__1 : rule__FMessageCollection__Group_5__1__Impl ;
    public final void rule__FMessageCollection__Group_5__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1773:1: ( rule__FMessageCollection__Group_5__1__Impl )
            // InternalDatatypes.g:1774:2: rule__FMessageCollection__Group_5__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FMessageCollection__Group_5__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group_5__1"


    // $ANTLR start "rule__FMessageCollection__Group_5__1__Impl"
    // InternalDatatypes.g:1780:1: rule__FMessageCollection__Group_5__1__Impl : ( ( rule__FMessageCollection__VersionAssignment_5_1 ) ) ;
    public final void rule__FMessageCollection__Group_5__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1784:1: ( ( ( rule__FMessageCollection__VersionAssignment_5_1 ) ) )
            // InternalDatatypes.g:1785:1: ( ( rule__FMessageCollection__VersionAssignment_5_1 ) )
            {
            // InternalDatatypes.g:1785:1: ( ( rule__FMessageCollection__VersionAssignment_5_1 ) )
            // InternalDatatypes.g:1786:2: ( rule__FMessageCollection__VersionAssignment_5_1 )
            {
             before(grammarAccess.getFMessageCollectionAccess().getVersionAssignment_5_1()); 
            // InternalDatatypes.g:1787:2: ( rule__FMessageCollection__VersionAssignment_5_1 )
            // InternalDatatypes.g:1787:3: rule__FMessageCollection__VersionAssignment_5_1
            {
            pushFollow(FOLLOW_2);
            rule__FMessageCollection__VersionAssignment_5_1();

            state._fsp--;


            }

             after(grammarAccess.getFMessageCollectionAccess().getVersionAssignment_5_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__Group_5__1__Impl"


    // $ANTLR start "rule__FMessage__Group__0"
    // InternalDatatypes.g:1796:1: rule__FMessage__Group__0 : rule__FMessage__Group__0__Impl rule__FMessage__Group__1 ;
    public final void rule__FMessage__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1800:1: ( rule__FMessage__Group__0__Impl rule__FMessage__Group__1 )
            // InternalDatatypes.g:1801:2: rule__FMessage__Group__0__Impl rule__FMessage__Group__1
            {
            pushFollow(FOLLOW_7);
            rule__FMessage__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMessage__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__Group__0"


    // $ANTLR start "rule__FMessage__Group__0__Impl"
    // InternalDatatypes.g:1808:1: rule__FMessage__Group__0__Impl : ( () ) ;
    public final void rule__FMessage__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1812:1: ( ( () ) )
            // InternalDatatypes.g:1813:1: ( () )
            {
            // InternalDatatypes.g:1813:1: ( () )
            // InternalDatatypes.g:1814:2: ()
            {
             before(grammarAccess.getFMessageAccess().getFMessageAction_0()); 
            // InternalDatatypes.g:1815:2: ()
            // InternalDatatypes.g:1815:3: 
            {
            }

             after(grammarAccess.getFMessageAccess().getFMessageAction_0()); 

            }


            }

        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__Group__0__Impl"


    // $ANTLR start "rule__FMessage__Group__1"
    // InternalDatatypes.g:1823:1: rule__FMessage__Group__1 : rule__FMessage__Group__1__Impl rule__FMessage__Group__2 ;
    public final void rule__FMessage__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1827:1: ( rule__FMessage__Group__1__Impl rule__FMessage__Group__2 )
            // InternalDatatypes.g:1828:2: rule__FMessage__Group__1__Impl rule__FMessage__Group__2
            {
            pushFollow(FOLLOW_7);
            rule__FMessage__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMessage__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__Group__1"


    // $ANTLR start "rule__FMessage__Group__1__Impl"
    // InternalDatatypes.g:1835:1: rule__FMessage__Group__1__Impl : ( ( rule__FMessage__DerivedAssignment_1 ) ) ;
    public final void rule__FMessage__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1839:1: ( ( ( rule__FMessage__DerivedAssignment_1 ) ) )
            // InternalDatatypes.g:1840:1: ( ( rule__FMessage__DerivedAssignment_1 ) )
            {
            // InternalDatatypes.g:1840:1: ( ( rule__FMessage__DerivedAssignment_1 ) )
            // InternalDatatypes.g:1841:2: ( rule__FMessage__DerivedAssignment_1 )
            {
             before(grammarAccess.getFMessageAccess().getDerivedAssignment_1()); 
            // InternalDatatypes.g:1842:2: ( rule__FMessage__DerivedAssignment_1 )
            // InternalDatatypes.g:1842:3: rule__FMessage__DerivedAssignment_1
            {
            pushFollow(FOLLOW_2);
            rule__FMessage__DerivedAssignment_1();

            state._fsp--;


            }

             after(grammarAccess.getFMessageAccess().getDerivedAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__Group__1__Impl"


    // $ANTLR start "rule__FMessage__Group__2"
    // InternalDatatypes.g:1850:1: rule__FMessage__Group__2 : rule__FMessage__Group__2__Impl rule__FMessage__Group__3 ;
    public final void rule__FMessage__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1854:1: ( rule__FMessage__Group__2__Impl rule__FMessage__Group__3 )
            // InternalDatatypes.g:1855:2: rule__FMessage__Group__2__Impl rule__FMessage__Group__3
            {
            pushFollow(FOLLOW_22);
            rule__FMessage__Group__2__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMessage__Group__3();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__Group__2"


    // $ANTLR start "rule__FMessage__Group__2__Impl"
    // InternalDatatypes.g:1862:1: rule__FMessage__Group__2__Impl : ( ( rule__FMessage__NameAssignment_2 ) ) ;
    public final void rule__FMessage__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1866:1: ( ( ( rule__FMessage__NameAssignment_2 ) ) )
            // InternalDatatypes.g:1867:1: ( ( rule__FMessage__NameAssignment_2 ) )
            {
            // InternalDatatypes.g:1867:1: ( ( rule__FMessage__NameAssignment_2 ) )
            // InternalDatatypes.g:1868:2: ( rule__FMessage__NameAssignment_2 )
            {
             before(grammarAccess.getFMessageAccess().getNameAssignment_2()); 
            // InternalDatatypes.g:1869:2: ( rule__FMessage__NameAssignment_2 )
            // InternalDatatypes.g:1869:3: rule__FMessage__NameAssignment_2
            {
            pushFollow(FOLLOW_2);
            rule__FMessage__NameAssignment_2();

            state._fsp--;


            }

             after(grammarAccess.getFMessageAccess().getNameAssignment_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__Group__2__Impl"


    // $ANTLR start "rule__FMessage__Group__3"
    // InternalDatatypes.g:1877:1: rule__FMessage__Group__3 : rule__FMessage__Group__3__Impl ;
    public final void rule__FMessage__Group__3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1881:1: ( rule__FMessage__Group__3__Impl )
            // InternalDatatypes.g:1882:2: rule__FMessage__Group__3__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FMessage__Group__3__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__Group__3"


    // $ANTLR start "rule__FMessage__Group__3__Impl"
    // InternalDatatypes.g:1888:1: rule__FMessage__Group__3__Impl : ( ( rule__FMessage__Group_3__0 )? ) ;
    public final void rule__FMessage__Group__3__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1892:1: ( ( ( rule__FMessage__Group_3__0 )? ) )
            // InternalDatatypes.g:1893:1: ( ( rule__FMessage__Group_3__0 )? )
            {
            // InternalDatatypes.g:1893:1: ( ( rule__FMessage__Group_3__0 )? )
            // InternalDatatypes.g:1894:2: ( rule__FMessage__Group_3__0 )?
            {
             before(grammarAccess.getFMessageAccess().getGroup_3()); 
            // InternalDatatypes.g:1895:2: ( rule__FMessage__Group_3__0 )?
            int alt18=2;
            int LA18_0 = input.LA(1);

            if ( (LA18_0==36) ) {
                alt18=1;
            }
            switch (alt18) {
                case 1 :
                    // InternalDatatypes.g:1895:3: rule__FMessage__Group_3__0
                    {
                    pushFollow(FOLLOW_2);
                    rule__FMessage__Group_3__0();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFMessageAccess().getGroup_3()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__Group__3__Impl"


    // $ANTLR start "rule__FMessage__Group_3__0"
    // InternalDatatypes.g:1904:1: rule__FMessage__Group_3__0 : rule__FMessage__Group_3__0__Impl rule__FMessage__Group_3__1 ;
    public final void rule__FMessage__Group_3__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1908:1: ( rule__FMessage__Group_3__0__Impl rule__FMessage__Group_3__1 )
            // InternalDatatypes.g:1909:2: rule__FMessage__Group_3__0__Impl rule__FMessage__Group_3__1
            {
            pushFollow(FOLLOW_7);
            rule__FMessage__Group_3__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMessage__Group_3__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__Group_3__0"


    // $ANTLR start "rule__FMessage__Group_3__0__Impl"
    // InternalDatatypes.g:1916:1: rule__FMessage__Group_3__0__Impl : ( 'key' ) ;
    public final void rule__FMessage__Group_3__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1920:1: ( ( 'key' ) )
            // InternalDatatypes.g:1921:1: ( 'key' )
            {
            // InternalDatatypes.g:1921:1: ( 'key' )
            // InternalDatatypes.g:1922:2: 'key'
            {
             before(grammarAccess.getFMessageAccess().getKeyKeyword_3_0()); 
            match(input,36,FOLLOW_2); 
             after(grammarAccess.getFMessageAccess().getKeyKeyword_3_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__Group_3__0__Impl"


    // $ANTLR start "rule__FMessage__Group_3__1"
    // InternalDatatypes.g:1931:1: rule__FMessage__Group_3__1 : rule__FMessage__Group_3__1__Impl ;
    public final void rule__FMessage__Group_3__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1935:1: ( rule__FMessage__Group_3__1__Impl )
            // InternalDatatypes.g:1936:2: rule__FMessage__Group_3__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FMessage__Group_3__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__Group_3__1"


    // $ANTLR start "rule__FMessage__Group_3__1__Impl"
    // InternalDatatypes.g:1942:1: rule__FMessage__Group_3__1__Impl : ( ( rule__FMessage__KeyAssignment_3_1 ) ) ;
    public final void rule__FMessage__Group_3__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1946:1: ( ( ( rule__FMessage__KeyAssignment_3_1 ) ) )
            // InternalDatatypes.g:1947:1: ( ( rule__FMessage__KeyAssignment_3_1 ) )
            {
            // InternalDatatypes.g:1947:1: ( ( rule__FMessage__KeyAssignment_3_1 ) )
            // InternalDatatypes.g:1948:2: ( rule__FMessage__KeyAssignment_3_1 )
            {
             before(grammarAccess.getFMessageAccess().getKeyAssignment_3_1()); 
            // InternalDatatypes.g:1949:2: ( rule__FMessage__KeyAssignment_3_1 )
            // InternalDatatypes.g:1949:3: rule__FMessage__KeyAssignment_3_1
            {
            pushFollow(FOLLOW_2);
            rule__FMessage__KeyAssignment_3_1();

            state._fsp--;


            }

             after(grammarAccess.getFMessageAccess().getKeyAssignment_3_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__Group_3__1__Impl"


    // $ANTLR start "rule__FVersion__Group__0"
    // InternalDatatypes.g:1958:1: rule__FVersion__Group__0 : rule__FVersion__Group__0__Impl rule__FVersion__Group__1 ;
    public final void rule__FVersion__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1962:1: ( rule__FVersion__Group__0__Impl rule__FVersion__Group__1 )
            // InternalDatatypes.g:1963:2: rule__FVersion__Group__0__Impl rule__FVersion__Group__1
            {
            pushFollow(FOLLOW_18);
            rule__FVersion__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FVersion__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__0"


    // $ANTLR start "rule__FVersion__Group__0__Impl"
    // InternalDatatypes.g:1970:1: rule__FVersion__Group__0__Impl : ( () ) ;
    public final void rule__FVersion__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1974:1: ( ( () ) )
            // InternalDatatypes.g:1975:1: ( () )
            {
            // InternalDatatypes.g:1975:1: ( () )
            // InternalDatatypes.g:1976:2: ()
            {
             before(grammarAccess.getFVersionAccess().getFVersionAction_0()); 
            // InternalDatatypes.g:1977:2: ()
            // InternalDatatypes.g:1977:3: 
            {
            }

             after(grammarAccess.getFVersionAccess().getFVersionAction_0()); 

            }


            }

        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__0__Impl"


    // $ANTLR start "rule__FVersion__Group__1"
    // InternalDatatypes.g:1985:1: rule__FVersion__Group__1 : rule__FVersion__Group__1__Impl rule__FVersion__Group__2 ;
    public final void rule__FVersion__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:1989:1: ( rule__FVersion__Group__1__Impl rule__FVersion__Group__2 )
            // InternalDatatypes.g:1990:2: rule__FVersion__Group__1__Impl rule__FVersion__Group__2
            {
            pushFollow(FOLLOW_23);
            rule__FVersion__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FVersion__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__1"


    // $ANTLR start "rule__FVersion__Group__1__Impl"
    // InternalDatatypes.g:1997:1: rule__FVersion__Group__1__Impl : ( '{' ) ;
    public final void rule__FVersion__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2001:1: ( ( '{' ) )
            // InternalDatatypes.g:2002:1: ( '{' )
            {
            // InternalDatatypes.g:2002:1: ( '{' )
            // InternalDatatypes.g:2003:2: '{'
            {
             before(grammarAccess.getFVersionAccess().getLeftCurlyBracketKeyword_1()); 
            match(input,32,FOLLOW_2); 
             after(grammarAccess.getFVersionAccess().getLeftCurlyBracketKeyword_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__1__Impl"


    // $ANTLR start "rule__FVersion__Group__2"
    // InternalDatatypes.g:2012:1: rule__FVersion__Group__2 : rule__FVersion__Group__2__Impl rule__FVersion__Group__3 ;
    public final void rule__FVersion__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2016:1: ( rule__FVersion__Group__2__Impl rule__FVersion__Group__3 )
            // InternalDatatypes.g:2017:2: rule__FVersion__Group__2__Impl rule__FVersion__Group__3
            {
            pushFollow(FOLLOW_24);
            rule__FVersion__Group__2__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FVersion__Group__3();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__2"


    // $ANTLR start "rule__FVersion__Group__2__Impl"
    // InternalDatatypes.g:2024:1: rule__FVersion__Group__2__Impl : ( 'major' ) ;
    public final void rule__FVersion__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2028:1: ( ( 'major' ) )
            // InternalDatatypes.g:2029:1: ( 'major' )
            {
            // InternalDatatypes.g:2029:1: ( 'major' )
            // InternalDatatypes.g:2030:2: 'major'
            {
             before(grammarAccess.getFVersionAccess().getMajorKeyword_2()); 
            match(input,37,FOLLOW_2); 
             after(grammarAccess.getFVersionAccess().getMajorKeyword_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__2__Impl"


    // $ANTLR start "rule__FVersion__Group__3"
    // InternalDatatypes.g:2039:1: rule__FVersion__Group__3 : rule__FVersion__Group__3__Impl rule__FVersion__Group__4 ;
    public final void rule__FVersion__Group__3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2043:1: ( rule__FVersion__Group__3__Impl rule__FVersion__Group__4 )
            // InternalDatatypes.g:2044:2: rule__FVersion__Group__3__Impl rule__FVersion__Group__4
            {
            pushFollow(FOLLOW_25);
            rule__FVersion__Group__3__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FVersion__Group__4();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__3"


    // $ANTLR start "rule__FVersion__Group__3__Impl"
    // InternalDatatypes.g:2051:1: rule__FVersion__Group__3__Impl : ( ( rule__FVersion__MajorAssignment_3 ) ) ;
    public final void rule__FVersion__Group__3__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2055:1: ( ( ( rule__FVersion__MajorAssignment_3 ) ) )
            // InternalDatatypes.g:2056:1: ( ( rule__FVersion__MajorAssignment_3 ) )
            {
            // InternalDatatypes.g:2056:1: ( ( rule__FVersion__MajorAssignment_3 ) )
            // InternalDatatypes.g:2057:2: ( rule__FVersion__MajorAssignment_3 )
            {
             before(grammarAccess.getFVersionAccess().getMajorAssignment_3()); 
            // InternalDatatypes.g:2058:2: ( rule__FVersion__MajorAssignment_3 )
            // InternalDatatypes.g:2058:3: rule__FVersion__MajorAssignment_3
            {
            pushFollow(FOLLOW_2);
            rule__FVersion__MajorAssignment_3();

            state._fsp--;


            }

             after(grammarAccess.getFVersionAccess().getMajorAssignment_3()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__3__Impl"


    // $ANTLR start "rule__FVersion__Group__4"
    // InternalDatatypes.g:2066:1: rule__FVersion__Group__4 : rule__FVersion__Group__4__Impl rule__FVersion__Group__5 ;
    public final void rule__FVersion__Group__4() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2070:1: ( rule__FVersion__Group__4__Impl rule__FVersion__Group__5 )
            // InternalDatatypes.g:2071:2: rule__FVersion__Group__4__Impl rule__FVersion__Group__5
            {
            pushFollow(FOLLOW_24);
            rule__FVersion__Group__4__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FVersion__Group__5();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__4"


    // $ANTLR start "rule__FVersion__Group__4__Impl"
    // InternalDatatypes.g:2078:1: rule__FVersion__Group__4__Impl : ( 'minor' ) ;
    public final void rule__FVersion__Group__4__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2082:1: ( ( 'minor' ) )
            // InternalDatatypes.g:2083:1: ( 'minor' )
            {
            // InternalDatatypes.g:2083:1: ( 'minor' )
            // InternalDatatypes.g:2084:2: 'minor'
            {
             before(grammarAccess.getFVersionAccess().getMinorKeyword_4()); 
            match(input,38,FOLLOW_2); 
             after(grammarAccess.getFVersionAccess().getMinorKeyword_4()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__4__Impl"


    // $ANTLR start "rule__FVersion__Group__5"
    // InternalDatatypes.g:2093:1: rule__FVersion__Group__5 : rule__FVersion__Group__5__Impl rule__FVersion__Group__6 ;
    public final void rule__FVersion__Group__5() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2097:1: ( rule__FVersion__Group__5__Impl rule__FVersion__Group__6 )
            // InternalDatatypes.g:2098:2: rule__FVersion__Group__5__Impl rule__FVersion__Group__6
            {
            pushFollow(FOLLOW_26);
            rule__FVersion__Group__5__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FVersion__Group__6();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__5"


    // $ANTLR start "rule__FVersion__Group__5__Impl"
    // InternalDatatypes.g:2105:1: rule__FVersion__Group__5__Impl : ( ( rule__FVersion__MinorAssignment_5 ) ) ;
    public final void rule__FVersion__Group__5__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2109:1: ( ( ( rule__FVersion__MinorAssignment_5 ) ) )
            // InternalDatatypes.g:2110:1: ( ( rule__FVersion__MinorAssignment_5 ) )
            {
            // InternalDatatypes.g:2110:1: ( ( rule__FVersion__MinorAssignment_5 ) )
            // InternalDatatypes.g:2111:2: ( rule__FVersion__MinorAssignment_5 )
            {
             before(grammarAccess.getFVersionAccess().getMinorAssignment_5()); 
            // InternalDatatypes.g:2112:2: ( rule__FVersion__MinorAssignment_5 )
            // InternalDatatypes.g:2112:3: rule__FVersion__MinorAssignment_5
            {
            pushFollow(FOLLOW_2);
            rule__FVersion__MinorAssignment_5();

            state._fsp--;


            }

             after(grammarAccess.getFVersionAccess().getMinorAssignment_5()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__5__Impl"


    // $ANTLR start "rule__FVersion__Group__6"
    // InternalDatatypes.g:2120:1: rule__FVersion__Group__6 : rule__FVersion__Group__6__Impl ;
    public final void rule__FVersion__Group__6() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2124:1: ( rule__FVersion__Group__6__Impl )
            // InternalDatatypes.g:2125:2: rule__FVersion__Group__6__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FVersion__Group__6__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__6"


    // $ANTLR start "rule__FVersion__Group__6__Impl"
    // InternalDatatypes.g:2131:1: rule__FVersion__Group__6__Impl : ( '}' ) ;
    public final void rule__FVersion__Group__6__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2135:1: ( ( '}' ) )
            // InternalDatatypes.g:2136:1: ( '}' )
            {
            // InternalDatatypes.g:2136:1: ( '}' )
            // InternalDatatypes.g:2137:2: '}'
            {
             before(grammarAccess.getFVersionAccess().getRightCurlyBracketKeyword_6()); 
            match(input,33,FOLLOW_2); 
             after(grammarAccess.getFVersionAccess().getRightCurlyBracketKeyword_6()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__Group__6__Impl"


    // $ANTLR start "rule__FArrayType__Group__0"
    // InternalDatatypes.g:2147:1: rule__FArrayType__Group__0 : rule__FArrayType__Group__0__Impl rule__FArrayType__Group__1 ;
    public final void rule__FArrayType__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2151:1: ( rule__FArrayType__Group__0__Impl rule__FArrayType__Group__1 )
            // InternalDatatypes.g:2152:2: rule__FArrayType__Group__0__Impl rule__FArrayType__Group__1
            {
            pushFollow(FOLLOW_27);
            rule__FArrayType__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FArrayType__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__Group__0"


    // $ANTLR start "rule__FArrayType__Group__0__Impl"
    // InternalDatatypes.g:2159:1: rule__FArrayType__Group__0__Impl : ( () ) ;
    public final void rule__FArrayType__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2163:1: ( ( () ) )
            // InternalDatatypes.g:2164:1: ( () )
            {
            // InternalDatatypes.g:2164:1: ( () )
            // InternalDatatypes.g:2165:2: ()
            {
             before(grammarAccess.getFArrayTypeAccess().getFArrayTypeAction_0()); 
            // InternalDatatypes.g:2166:2: ()
            // InternalDatatypes.g:2166:3: 
            {
            }

             after(grammarAccess.getFArrayTypeAccess().getFArrayTypeAction_0()); 

            }


            }

        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__Group__0__Impl"


    // $ANTLR start "rule__FArrayType__Group__1"
    // InternalDatatypes.g:2174:1: rule__FArrayType__Group__1 : rule__FArrayType__Group__1__Impl rule__FArrayType__Group__2 ;
    public final void rule__FArrayType__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2178:1: ( rule__FArrayType__Group__1__Impl rule__FArrayType__Group__2 )
            // InternalDatatypes.g:2179:2: rule__FArrayType__Group__1__Impl rule__FArrayType__Group__2
            {
            pushFollow(FOLLOW_27);
            rule__FArrayType__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FArrayType__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__Group__1"


    // $ANTLR start "rule__FArrayType__Group__1__Impl"
    // InternalDatatypes.g:2186:1: rule__FArrayType__Group__1__Impl : ( ( rule__FArrayType__CommentAssignment_1 )? ) ;
    public final void rule__FArrayType__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2190:1: ( ( ( rule__FArrayType__CommentAssignment_1 )? ) )
            // InternalDatatypes.g:2191:1: ( ( rule__FArrayType__CommentAssignment_1 )? )
            {
            // InternalDatatypes.g:2191:1: ( ( rule__FArrayType__CommentAssignment_1 )? )
            // InternalDatatypes.g:2192:2: ( rule__FArrayType__CommentAssignment_1 )?
            {
             before(grammarAccess.getFArrayTypeAccess().getCommentAssignment_1()); 
            // InternalDatatypes.g:2193:2: ( rule__FArrayType__CommentAssignment_1 )?
            int alt19=2;
            int LA19_0 = input.LA(1);

            if ( (LA19_0==29) ) {
                alt19=1;
            }
            switch (alt19) {
                case 1 :
                    // InternalDatatypes.g:2193:3: rule__FArrayType__CommentAssignment_1
                    {
                    pushFollow(FOLLOW_2);
                    rule__FArrayType__CommentAssignment_1();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFArrayTypeAccess().getCommentAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__Group__1__Impl"


    // $ANTLR start "rule__FArrayType__Group__2"
    // InternalDatatypes.g:2201:1: rule__FArrayType__Group__2 : rule__FArrayType__Group__2__Impl rule__FArrayType__Group__3 ;
    public final void rule__FArrayType__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2205:1: ( rule__FArrayType__Group__2__Impl rule__FArrayType__Group__3 )
            // InternalDatatypes.g:2206:2: rule__FArrayType__Group__2__Impl rule__FArrayType__Group__3
            {
            pushFollow(FOLLOW_7);
            rule__FArrayType__Group__2__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FArrayType__Group__3();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__Group__2"


    // $ANTLR start "rule__FArrayType__Group__2__Impl"
    // InternalDatatypes.g:2213:1: rule__FArrayType__Group__2__Impl : ( 'array' ) ;
    public final void rule__FArrayType__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2217:1: ( ( 'array' ) )
            // InternalDatatypes.g:2218:1: ( 'array' )
            {
            // InternalDatatypes.g:2218:1: ( 'array' )
            // InternalDatatypes.g:2219:2: 'array'
            {
             before(grammarAccess.getFArrayTypeAccess().getArrayKeyword_2()); 
            match(input,39,FOLLOW_2); 
             after(grammarAccess.getFArrayTypeAccess().getArrayKeyword_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__Group__2__Impl"


    // $ANTLR start "rule__FArrayType__Group__3"
    // InternalDatatypes.g:2228:1: rule__FArrayType__Group__3 : rule__FArrayType__Group__3__Impl rule__FArrayType__Group__4 ;
    public final void rule__FArrayType__Group__3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2232:1: ( rule__FArrayType__Group__3__Impl rule__FArrayType__Group__4 )
            // InternalDatatypes.g:2233:2: rule__FArrayType__Group__3__Impl rule__FArrayType__Group__4
            {
            pushFollow(FOLLOW_28);
            rule__FArrayType__Group__3__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FArrayType__Group__4();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__Group__3"


    // $ANTLR start "rule__FArrayType__Group__3__Impl"
    // InternalDatatypes.g:2240:1: rule__FArrayType__Group__3__Impl : ( ( rule__FArrayType__NameAssignment_3 ) ) ;
    public final void rule__FArrayType__Group__3__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2244:1: ( ( ( rule__FArrayType__NameAssignment_3 ) ) )
            // InternalDatatypes.g:2245:1: ( ( rule__FArrayType__NameAssignment_3 ) )
            {
            // InternalDatatypes.g:2245:1: ( ( rule__FArrayType__NameAssignment_3 ) )
            // InternalDatatypes.g:2246:2: ( rule__FArrayType__NameAssignment_3 )
            {
             before(grammarAccess.getFArrayTypeAccess().getNameAssignment_3()); 
            // InternalDatatypes.g:2247:2: ( rule__FArrayType__NameAssignment_3 )
            // InternalDatatypes.g:2247:3: rule__FArrayType__NameAssignment_3
            {
            pushFollow(FOLLOW_2);
            rule__FArrayType__NameAssignment_3();

            state._fsp--;


            }

             after(grammarAccess.getFArrayTypeAccess().getNameAssignment_3()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__Group__3__Impl"


    // $ANTLR start "rule__FArrayType__Group__4"
    // InternalDatatypes.g:2255:1: rule__FArrayType__Group__4 : rule__FArrayType__Group__4__Impl rule__FArrayType__Group__5 ;
    public final void rule__FArrayType__Group__4() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2259:1: ( rule__FArrayType__Group__4__Impl rule__FArrayType__Group__5 )
            // InternalDatatypes.g:2260:2: rule__FArrayType__Group__4__Impl rule__FArrayType__Group__5
            {
            pushFollow(FOLLOW_29);
            rule__FArrayType__Group__4__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FArrayType__Group__5();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__Group__4"


    // $ANTLR start "rule__FArrayType__Group__4__Impl"
    // InternalDatatypes.g:2267:1: rule__FArrayType__Group__4__Impl : ( 'of' ) ;
    public final void rule__FArrayType__Group__4__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2271:1: ( ( 'of' ) )
            // InternalDatatypes.g:2272:1: ( 'of' )
            {
            // InternalDatatypes.g:2272:1: ( 'of' )
            // InternalDatatypes.g:2273:2: 'of'
            {
             before(grammarAccess.getFArrayTypeAccess().getOfKeyword_4()); 
            match(input,40,FOLLOW_2); 
             after(grammarAccess.getFArrayTypeAccess().getOfKeyword_4()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__Group__4__Impl"


    // $ANTLR start "rule__FArrayType__Group__5"
    // InternalDatatypes.g:2282:1: rule__FArrayType__Group__5 : rule__FArrayType__Group__5__Impl ;
    public final void rule__FArrayType__Group__5() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2286:1: ( rule__FArrayType__Group__5__Impl )
            // InternalDatatypes.g:2287:2: rule__FArrayType__Group__5__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FArrayType__Group__5__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__Group__5"


    // $ANTLR start "rule__FArrayType__Group__5__Impl"
    // InternalDatatypes.g:2293:1: rule__FArrayType__Group__5__Impl : ( ( rule__FArrayType__ElementTypeAssignment_5 ) ) ;
    public final void rule__FArrayType__Group__5__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2297:1: ( ( ( rule__FArrayType__ElementTypeAssignment_5 ) ) )
            // InternalDatatypes.g:2298:1: ( ( rule__FArrayType__ElementTypeAssignment_5 ) )
            {
            // InternalDatatypes.g:2298:1: ( ( rule__FArrayType__ElementTypeAssignment_5 ) )
            // InternalDatatypes.g:2299:2: ( rule__FArrayType__ElementTypeAssignment_5 )
            {
             before(grammarAccess.getFArrayTypeAccess().getElementTypeAssignment_5()); 
            // InternalDatatypes.g:2300:2: ( rule__FArrayType__ElementTypeAssignment_5 )
            // InternalDatatypes.g:2300:3: rule__FArrayType__ElementTypeAssignment_5
            {
            pushFollow(FOLLOW_2);
            rule__FArrayType__ElementTypeAssignment_5();

            state._fsp--;


            }

             after(grammarAccess.getFArrayTypeAccess().getElementTypeAssignment_5()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__Group__5__Impl"


    // $ANTLR start "rule__FTypeDef__Group__0"
    // InternalDatatypes.g:2309:1: rule__FTypeDef__Group__0 : rule__FTypeDef__Group__0__Impl rule__FTypeDef__Group__1 ;
    public final void rule__FTypeDef__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2313:1: ( rule__FTypeDef__Group__0__Impl rule__FTypeDef__Group__1 )
            // InternalDatatypes.g:2314:2: rule__FTypeDef__Group__0__Impl rule__FTypeDef__Group__1
            {
            pushFollow(FOLLOW_30);
            rule__FTypeDef__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeDef__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__Group__0"


    // $ANTLR start "rule__FTypeDef__Group__0__Impl"
    // InternalDatatypes.g:2321:1: rule__FTypeDef__Group__0__Impl : ( () ) ;
    public final void rule__FTypeDef__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2325:1: ( ( () ) )
            // InternalDatatypes.g:2326:1: ( () )
            {
            // InternalDatatypes.g:2326:1: ( () )
            // InternalDatatypes.g:2327:2: ()
            {
             before(grammarAccess.getFTypeDefAccess().getFTypeDefAction_0()); 
            // InternalDatatypes.g:2328:2: ()
            // InternalDatatypes.g:2328:3: 
            {
            }

             after(grammarAccess.getFTypeDefAccess().getFTypeDefAction_0()); 

            }


            }

        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__Group__0__Impl"


    // $ANTLR start "rule__FTypeDef__Group__1"
    // InternalDatatypes.g:2336:1: rule__FTypeDef__Group__1 : rule__FTypeDef__Group__1__Impl rule__FTypeDef__Group__2 ;
    public final void rule__FTypeDef__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2340:1: ( rule__FTypeDef__Group__1__Impl rule__FTypeDef__Group__2 )
            // InternalDatatypes.g:2341:2: rule__FTypeDef__Group__1__Impl rule__FTypeDef__Group__2
            {
            pushFollow(FOLLOW_30);
            rule__FTypeDef__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeDef__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__Group__1"


    // $ANTLR start "rule__FTypeDef__Group__1__Impl"
    // InternalDatatypes.g:2348:1: rule__FTypeDef__Group__1__Impl : ( ( rule__FTypeDef__CommentAssignment_1 )? ) ;
    public final void rule__FTypeDef__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2352:1: ( ( ( rule__FTypeDef__CommentAssignment_1 )? ) )
            // InternalDatatypes.g:2353:1: ( ( rule__FTypeDef__CommentAssignment_1 )? )
            {
            // InternalDatatypes.g:2353:1: ( ( rule__FTypeDef__CommentAssignment_1 )? )
            // InternalDatatypes.g:2354:2: ( rule__FTypeDef__CommentAssignment_1 )?
            {
             before(grammarAccess.getFTypeDefAccess().getCommentAssignment_1()); 
            // InternalDatatypes.g:2355:2: ( rule__FTypeDef__CommentAssignment_1 )?
            int alt20=2;
            int LA20_0 = input.LA(1);

            if ( (LA20_0==29) ) {
                alt20=1;
            }
            switch (alt20) {
                case 1 :
                    // InternalDatatypes.g:2355:3: rule__FTypeDef__CommentAssignment_1
                    {
                    pushFollow(FOLLOW_2);
                    rule__FTypeDef__CommentAssignment_1();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFTypeDefAccess().getCommentAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__Group__1__Impl"


    // $ANTLR start "rule__FTypeDef__Group__2"
    // InternalDatatypes.g:2363:1: rule__FTypeDef__Group__2 : rule__FTypeDef__Group__2__Impl rule__FTypeDef__Group__3 ;
    public final void rule__FTypeDef__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2367:1: ( rule__FTypeDef__Group__2__Impl rule__FTypeDef__Group__3 )
            // InternalDatatypes.g:2368:2: rule__FTypeDef__Group__2__Impl rule__FTypeDef__Group__3
            {
            pushFollow(FOLLOW_7);
            rule__FTypeDef__Group__2__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeDef__Group__3();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__Group__2"


    // $ANTLR start "rule__FTypeDef__Group__2__Impl"
    // InternalDatatypes.g:2375:1: rule__FTypeDef__Group__2__Impl : ( 'typedef' ) ;
    public final void rule__FTypeDef__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2379:1: ( ( 'typedef' ) )
            // InternalDatatypes.g:2380:1: ( 'typedef' )
            {
            // InternalDatatypes.g:2380:1: ( 'typedef' )
            // InternalDatatypes.g:2381:2: 'typedef'
            {
             before(grammarAccess.getFTypeDefAccess().getTypedefKeyword_2()); 
            match(input,41,FOLLOW_2); 
             after(grammarAccess.getFTypeDefAccess().getTypedefKeyword_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__Group__2__Impl"


    // $ANTLR start "rule__FTypeDef__Group__3"
    // InternalDatatypes.g:2390:1: rule__FTypeDef__Group__3 : rule__FTypeDef__Group__3__Impl rule__FTypeDef__Group__4 ;
    public final void rule__FTypeDef__Group__3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2394:1: ( rule__FTypeDef__Group__3__Impl rule__FTypeDef__Group__4 )
            // InternalDatatypes.g:2395:2: rule__FTypeDef__Group__3__Impl rule__FTypeDef__Group__4
            {
            pushFollow(FOLLOW_31);
            rule__FTypeDef__Group__3__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeDef__Group__4();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__Group__3"


    // $ANTLR start "rule__FTypeDef__Group__3__Impl"
    // InternalDatatypes.g:2402:1: rule__FTypeDef__Group__3__Impl : ( ( rule__FTypeDef__NameAssignment_3 ) ) ;
    public final void rule__FTypeDef__Group__3__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2406:1: ( ( ( rule__FTypeDef__NameAssignment_3 ) ) )
            // InternalDatatypes.g:2407:1: ( ( rule__FTypeDef__NameAssignment_3 ) )
            {
            // InternalDatatypes.g:2407:1: ( ( rule__FTypeDef__NameAssignment_3 ) )
            // InternalDatatypes.g:2408:2: ( rule__FTypeDef__NameAssignment_3 )
            {
             before(grammarAccess.getFTypeDefAccess().getNameAssignment_3()); 
            // InternalDatatypes.g:2409:2: ( rule__FTypeDef__NameAssignment_3 )
            // InternalDatatypes.g:2409:3: rule__FTypeDef__NameAssignment_3
            {
            pushFollow(FOLLOW_2);
            rule__FTypeDef__NameAssignment_3();

            state._fsp--;


            }

             after(grammarAccess.getFTypeDefAccess().getNameAssignment_3()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__Group__3__Impl"


    // $ANTLR start "rule__FTypeDef__Group__4"
    // InternalDatatypes.g:2417:1: rule__FTypeDef__Group__4 : rule__FTypeDef__Group__4__Impl rule__FTypeDef__Group__5 ;
    public final void rule__FTypeDef__Group__4() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2421:1: ( rule__FTypeDef__Group__4__Impl rule__FTypeDef__Group__5 )
            // InternalDatatypes.g:2422:2: rule__FTypeDef__Group__4__Impl rule__FTypeDef__Group__5
            {
            pushFollow(FOLLOW_29);
            rule__FTypeDef__Group__4__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FTypeDef__Group__5();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__Group__4"


    // $ANTLR start "rule__FTypeDef__Group__4__Impl"
    // InternalDatatypes.g:2429:1: rule__FTypeDef__Group__4__Impl : ( 'is' ) ;
    public final void rule__FTypeDef__Group__4__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2433:1: ( ( 'is' ) )
            // InternalDatatypes.g:2434:1: ( 'is' )
            {
            // InternalDatatypes.g:2434:1: ( 'is' )
            // InternalDatatypes.g:2435:2: 'is'
            {
             before(grammarAccess.getFTypeDefAccess().getIsKeyword_4()); 
            match(input,42,FOLLOW_2); 
             after(grammarAccess.getFTypeDefAccess().getIsKeyword_4()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__Group__4__Impl"


    // $ANTLR start "rule__FTypeDef__Group__5"
    // InternalDatatypes.g:2444:1: rule__FTypeDef__Group__5 : rule__FTypeDef__Group__5__Impl ;
    public final void rule__FTypeDef__Group__5() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2448:1: ( rule__FTypeDef__Group__5__Impl )
            // InternalDatatypes.g:2449:2: rule__FTypeDef__Group__5__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FTypeDef__Group__5__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__Group__5"


    // $ANTLR start "rule__FTypeDef__Group__5__Impl"
    // InternalDatatypes.g:2455:1: rule__FTypeDef__Group__5__Impl : ( ( rule__FTypeDef__ActualTypeAssignment_5 ) ) ;
    public final void rule__FTypeDef__Group__5__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2459:1: ( ( ( rule__FTypeDef__ActualTypeAssignment_5 ) ) )
            // InternalDatatypes.g:2460:1: ( ( rule__FTypeDef__ActualTypeAssignment_5 ) )
            {
            // InternalDatatypes.g:2460:1: ( ( rule__FTypeDef__ActualTypeAssignment_5 ) )
            // InternalDatatypes.g:2461:2: ( rule__FTypeDef__ActualTypeAssignment_5 )
            {
             before(grammarAccess.getFTypeDefAccess().getActualTypeAssignment_5()); 
            // InternalDatatypes.g:2462:2: ( rule__FTypeDef__ActualTypeAssignment_5 )
            // InternalDatatypes.g:2462:3: rule__FTypeDef__ActualTypeAssignment_5
            {
            pushFollow(FOLLOW_2);
            rule__FTypeDef__ActualTypeAssignment_5();

            state._fsp--;


            }

             after(grammarAccess.getFTypeDefAccess().getActualTypeAssignment_5()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__Group__5__Impl"


    // $ANTLR start "rule__FStructType__Group__0"
    // InternalDatatypes.g:2471:1: rule__FStructType__Group__0 : rule__FStructType__Group__0__Impl rule__FStructType__Group__1 ;
    public final void rule__FStructType__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2475:1: ( rule__FStructType__Group__0__Impl rule__FStructType__Group__1 )
            // InternalDatatypes.g:2476:2: rule__FStructType__Group__0__Impl rule__FStructType__Group__1
            {
            pushFollow(FOLLOW_32);
            rule__FStructType__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FStructType__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__0"


    // $ANTLR start "rule__FStructType__Group__0__Impl"
    // InternalDatatypes.g:2483:1: rule__FStructType__Group__0__Impl : ( () ) ;
    public final void rule__FStructType__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2487:1: ( ( () ) )
            // InternalDatatypes.g:2488:1: ( () )
            {
            // InternalDatatypes.g:2488:1: ( () )
            // InternalDatatypes.g:2489:2: ()
            {
             before(grammarAccess.getFStructTypeAccess().getFStructTypeAction_0()); 
            // InternalDatatypes.g:2490:2: ()
            // InternalDatatypes.g:2490:3: 
            {
            }

             after(grammarAccess.getFStructTypeAccess().getFStructTypeAction_0()); 

            }


            }

        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__0__Impl"


    // $ANTLR start "rule__FStructType__Group__1"
    // InternalDatatypes.g:2498:1: rule__FStructType__Group__1 : rule__FStructType__Group__1__Impl rule__FStructType__Group__2 ;
    public final void rule__FStructType__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2502:1: ( rule__FStructType__Group__1__Impl rule__FStructType__Group__2 )
            // InternalDatatypes.g:2503:2: rule__FStructType__Group__1__Impl rule__FStructType__Group__2
            {
            pushFollow(FOLLOW_32);
            rule__FStructType__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FStructType__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__1"


    // $ANTLR start "rule__FStructType__Group__1__Impl"
    // InternalDatatypes.g:2510:1: rule__FStructType__Group__1__Impl : ( ( rule__FStructType__CommentAssignment_1 )? ) ;
    public final void rule__FStructType__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2514:1: ( ( ( rule__FStructType__CommentAssignment_1 )? ) )
            // InternalDatatypes.g:2515:1: ( ( rule__FStructType__CommentAssignment_1 )? )
            {
            // InternalDatatypes.g:2515:1: ( ( rule__FStructType__CommentAssignment_1 )? )
            // InternalDatatypes.g:2516:2: ( rule__FStructType__CommentAssignment_1 )?
            {
             before(grammarAccess.getFStructTypeAccess().getCommentAssignment_1()); 
            // InternalDatatypes.g:2517:2: ( rule__FStructType__CommentAssignment_1 )?
            int alt21=2;
            int LA21_0 = input.LA(1);

            if ( (LA21_0==29) ) {
                alt21=1;
            }
            switch (alt21) {
                case 1 :
                    // InternalDatatypes.g:2517:3: rule__FStructType__CommentAssignment_1
                    {
                    pushFollow(FOLLOW_2);
                    rule__FStructType__CommentAssignment_1();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFStructTypeAccess().getCommentAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__1__Impl"


    // $ANTLR start "rule__FStructType__Group__2"
    // InternalDatatypes.g:2525:1: rule__FStructType__Group__2 : rule__FStructType__Group__2__Impl rule__FStructType__Group__3 ;
    public final void rule__FStructType__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2529:1: ( rule__FStructType__Group__2__Impl rule__FStructType__Group__3 )
            // InternalDatatypes.g:2530:2: rule__FStructType__Group__2__Impl rule__FStructType__Group__3
            {
            pushFollow(FOLLOW_7);
            rule__FStructType__Group__2__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FStructType__Group__3();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__2"


    // $ANTLR start "rule__FStructType__Group__2__Impl"
    // InternalDatatypes.g:2537:1: rule__FStructType__Group__2__Impl : ( 'struct' ) ;
    public final void rule__FStructType__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2541:1: ( ( 'struct' ) )
            // InternalDatatypes.g:2542:1: ( 'struct' )
            {
            // InternalDatatypes.g:2542:1: ( 'struct' )
            // InternalDatatypes.g:2543:2: 'struct'
            {
             before(grammarAccess.getFStructTypeAccess().getStructKeyword_2()); 
            match(input,43,FOLLOW_2); 
             after(grammarAccess.getFStructTypeAccess().getStructKeyword_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__2__Impl"


    // $ANTLR start "rule__FStructType__Group__3"
    // InternalDatatypes.g:2552:1: rule__FStructType__Group__3 : rule__FStructType__Group__3__Impl rule__FStructType__Group__4 ;
    public final void rule__FStructType__Group__3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2556:1: ( rule__FStructType__Group__3__Impl rule__FStructType__Group__4 )
            // InternalDatatypes.g:2557:2: rule__FStructType__Group__3__Impl rule__FStructType__Group__4
            {
            pushFollow(FOLLOW_33);
            rule__FStructType__Group__3__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FStructType__Group__4();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__3"


    // $ANTLR start "rule__FStructType__Group__3__Impl"
    // InternalDatatypes.g:2564:1: rule__FStructType__Group__3__Impl : ( ( rule__FStructType__NameAssignment_3 ) ) ;
    public final void rule__FStructType__Group__3__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2568:1: ( ( ( rule__FStructType__NameAssignment_3 ) ) )
            // InternalDatatypes.g:2569:1: ( ( rule__FStructType__NameAssignment_3 ) )
            {
            // InternalDatatypes.g:2569:1: ( ( rule__FStructType__NameAssignment_3 ) )
            // InternalDatatypes.g:2570:2: ( rule__FStructType__NameAssignment_3 )
            {
             before(grammarAccess.getFStructTypeAccess().getNameAssignment_3()); 
            // InternalDatatypes.g:2571:2: ( rule__FStructType__NameAssignment_3 )
            // InternalDatatypes.g:2571:3: rule__FStructType__NameAssignment_3
            {
            pushFollow(FOLLOW_2);
            rule__FStructType__NameAssignment_3();

            state._fsp--;


            }

             after(grammarAccess.getFStructTypeAccess().getNameAssignment_3()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__3__Impl"


    // $ANTLR start "rule__FStructType__Group__4"
    // InternalDatatypes.g:2579:1: rule__FStructType__Group__4 : rule__FStructType__Group__4__Impl rule__FStructType__Group__5 ;
    public final void rule__FStructType__Group__4() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2583:1: ( rule__FStructType__Group__4__Impl rule__FStructType__Group__5 )
            // InternalDatatypes.g:2584:2: rule__FStructType__Group__4__Impl rule__FStructType__Group__5
            {
            pushFollow(FOLLOW_33);
            rule__FStructType__Group__4__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FStructType__Group__5();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__4"


    // $ANTLR start "rule__FStructType__Group__4__Impl"
    // InternalDatatypes.g:2591:1: rule__FStructType__Group__4__Impl : ( ( rule__FStructType__Group_4__0 )? ) ;
    public final void rule__FStructType__Group__4__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2595:1: ( ( ( rule__FStructType__Group_4__0 )? ) )
            // InternalDatatypes.g:2596:1: ( ( rule__FStructType__Group_4__0 )? )
            {
            // InternalDatatypes.g:2596:1: ( ( rule__FStructType__Group_4__0 )? )
            // InternalDatatypes.g:2597:2: ( rule__FStructType__Group_4__0 )?
            {
             before(grammarAccess.getFStructTypeAccess().getGroup_4()); 
            // InternalDatatypes.g:2598:2: ( rule__FStructType__Group_4__0 )?
            int alt22=2;
            int LA22_0 = input.LA(1);

            if ( (LA22_0==44) ) {
                alt22=1;
            }
            switch (alt22) {
                case 1 :
                    // InternalDatatypes.g:2598:3: rule__FStructType__Group_4__0
                    {
                    pushFollow(FOLLOW_2);
                    rule__FStructType__Group_4__0();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFStructTypeAccess().getGroup_4()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__4__Impl"


    // $ANTLR start "rule__FStructType__Group__5"
    // InternalDatatypes.g:2606:1: rule__FStructType__Group__5 : rule__FStructType__Group__5__Impl rule__FStructType__Group__6 ;
    public final void rule__FStructType__Group__5() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2610:1: ( rule__FStructType__Group__5__Impl rule__FStructType__Group__6 )
            // InternalDatatypes.g:2611:2: rule__FStructType__Group__5__Impl rule__FStructType__Group__6
            {
            pushFollow(FOLLOW_34);
            rule__FStructType__Group__5__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FStructType__Group__6();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__5"


    // $ANTLR start "rule__FStructType__Group__5__Impl"
    // InternalDatatypes.g:2618:1: rule__FStructType__Group__5__Impl : ( '{' ) ;
    public final void rule__FStructType__Group__5__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2622:1: ( ( '{' ) )
            // InternalDatatypes.g:2623:1: ( '{' )
            {
            // InternalDatatypes.g:2623:1: ( '{' )
            // InternalDatatypes.g:2624:2: '{'
            {
             before(grammarAccess.getFStructTypeAccess().getLeftCurlyBracketKeyword_5()); 
            match(input,32,FOLLOW_2); 
             after(grammarAccess.getFStructTypeAccess().getLeftCurlyBracketKeyword_5()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__5__Impl"


    // $ANTLR start "rule__FStructType__Group__6"
    // InternalDatatypes.g:2633:1: rule__FStructType__Group__6 : rule__FStructType__Group__6__Impl rule__FStructType__Group__7 ;
    public final void rule__FStructType__Group__6() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2637:1: ( rule__FStructType__Group__6__Impl rule__FStructType__Group__7 )
            // InternalDatatypes.g:2638:2: rule__FStructType__Group__6__Impl rule__FStructType__Group__7
            {
            pushFollow(FOLLOW_34);
            rule__FStructType__Group__6__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FStructType__Group__7();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__6"


    // $ANTLR start "rule__FStructType__Group__6__Impl"
    // InternalDatatypes.g:2645:1: rule__FStructType__Group__6__Impl : ( ( rule__FStructType__ElementsAssignment_6 )* ) ;
    public final void rule__FStructType__Group__6__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2649:1: ( ( ( rule__FStructType__ElementsAssignment_6 )* ) )
            // InternalDatatypes.g:2650:1: ( ( rule__FStructType__ElementsAssignment_6 )* )
            {
            // InternalDatatypes.g:2650:1: ( ( rule__FStructType__ElementsAssignment_6 )* )
            // InternalDatatypes.g:2651:2: ( rule__FStructType__ElementsAssignment_6 )*
            {
             before(grammarAccess.getFStructTypeAccess().getElementsAssignment_6()); 
            // InternalDatatypes.g:2652:2: ( rule__FStructType__ElementsAssignment_6 )*
            loop23:
            do {
                int alt23=2;
                int LA23_0 = input.LA(1);

                if ( (LA23_0==RULE_ID||(LA23_0>=12 && LA23_0<=24)||LA23_0==29) ) {
                    alt23=1;
                }


                switch (alt23) {
            	case 1 :
            	    // InternalDatatypes.g:2652:3: rule__FStructType__ElementsAssignment_6
            	    {
            	    pushFollow(FOLLOW_35);
            	    rule__FStructType__ElementsAssignment_6();

            	    state._fsp--;


            	    }
            	    break;

            	default :
            	    break loop23;
                }
            } while (true);

             after(grammarAccess.getFStructTypeAccess().getElementsAssignment_6()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__6__Impl"


    // $ANTLR start "rule__FStructType__Group__7"
    // InternalDatatypes.g:2660:1: rule__FStructType__Group__7 : rule__FStructType__Group__7__Impl ;
    public final void rule__FStructType__Group__7() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2664:1: ( rule__FStructType__Group__7__Impl )
            // InternalDatatypes.g:2665:2: rule__FStructType__Group__7__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FStructType__Group__7__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__7"


    // $ANTLR start "rule__FStructType__Group__7__Impl"
    // InternalDatatypes.g:2671:1: rule__FStructType__Group__7__Impl : ( '}' ) ;
    public final void rule__FStructType__Group__7__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2675:1: ( ( '}' ) )
            // InternalDatatypes.g:2676:1: ( '}' )
            {
            // InternalDatatypes.g:2676:1: ( '}' )
            // InternalDatatypes.g:2677:2: '}'
            {
             before(grammarAccess.getFStructTypeAccess().getRightCurlyBracketKeyword_7()); 
            match(input,33,FOLLOW_2); 
             after(grammarAccess.getFStructTypeAccess().getRightCurlyBracketKeyword_7()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group__7__Impl"


    // $ANTLR start "rule__FStructType__Group_4__0"
    // InternalDatatypes.g:2687:1: rule__FStructType__Group_4__0 : rule__FStructType__Group_4__0__Impl rule__FStructType__Group_4__1 ;
    public final void rule__FStructType__Group_4__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2691:1: ( rule__FStructType__Group_4__0__Impl rule__FStructType__Group_4__1 )
            // InternalDatatypes.g:2692:2: rule__FStructType__Group_4__0__Impl rule__FStructType__Group_4__1
            {
            pushFollow(FOLLOW_7);
            rule__FStructType__Group_4__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FStructType__Group_4__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group_4__0"


    // $ANTLR start "rule__FStructType__Group_4__0__Impl"
    // InternalDatatypes.g:2699:1: rule__FStructType__Group_4__0__Impl : ( 'extends' ) ;
    public final void rule__FStructType__Group_4__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2703:1: ( ( 'extends' ) )
            // InternalDatatypes.g:2704:1: ( 'extends' )
            {
            // InternalDatatypes.g:2704:1: ( 'extends' )
            // InternalDatatypes.g:2705:2: 'extends'
            {
             before(grammarAccess.getFStructTypeAccess().getExtendsKeyword_4_0()); 
            match(input,44,FOLLOW_2); 
             after(grammarAccess.getFStructTypeAccess().getExtendsKeyword_4_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group_4__0__Impl"


    // $ANTLR start "rule__FStructType__Group_4__1"
    // InternalDatatypes.g:2714:1: rule__FStructType__Group_4__1 : rule__FStructType__Group_4__1__Impl ;
    public final void rule__FStructType__Group_4__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2718:1: ( rule__FStructType__Group_4__1__Impl )
            // InternalDatatypes.g:2719:2: rule__FStructType__Group_4__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FStructType__Group_4__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group_4__1"


    // $ANTLR start "rule__FStructType__Group_4__1__Impl"
    // InternalDatatypes.g:2725:1: rule__FStructType__Group_4__1__Impl : ( ( rule__FStructType__BaseAssignment_4_1 ) ) ;
    public final void rule__FStructType__Group_4__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2729:1: ( ( ( rule__FStructType__BaseAssignment_4_1 ) ) )
            // InternalDatatypes.g:2730:1: ( ( rule__FStructType__BaseAssignment_4_1 ) )
            {
            // InternalDatatypes.g:2730:1: ( ( rule__FStructType__BaseAssignment_4_1 ) )
            // InternalDatatypes.g:2731:2: ( rule__FStructType__BaseAssignment_4_1 )
            {
             before(grammarAccess.getFStructTypeAccess().getBaseAssignment_4_1()); 
            // InternalDatatypes.g:2732:2: ( rule__FStructType__BaseAssignment_4_1 )
            // InternalDatatypes.g:2732:3: rule__FStructType__BaseAssignment_4_1
            {
            pushFollow(FOLLOW_2);
            rule__FStructType__BaseAssignment_4_1();

            state._fsp--;


            }

             after(grammarAccess.getFStructTypeAccess().getBaseAssignment_4_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__Group_4__1__Impl"


    // $ANTLR start "rule__FEnumerationType__Group__0"
    // InternalDatatypes.g:2741:1: rule__FEnumerationType__Group__0 : rule__FEnumerationType__Group__0__Impl rule__FEnumerationType__Group__1 ;
    public final void rule__FEnumerationType__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2745:1: ( rule__FEnumerationType__Group__0__Impl rule__FEnumerationType__Group__1 )
            // InternalDatatypes.g:2746:2: rule__FEnumerationType__Group__0__Impl rule__FEnumerationType__Group__1
            {
            pushFollow(FOLLOW_36);
            rule__FEnumerationType__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__0"


    // $ANTLR start "rule__FEnumerationType__Group__0__Impl"
    // InternalDatatypes.g:2753:1: rule__FEnumerationType__Group__0__Impl : ( () ) ;
    public final void rule__FEnumerationType__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2757:1: ( ( () ) )
            // InternalDatatypes.g:2758:1: ( () )
            {
            // InternalDatatypes.g:2758:1: ( () )
            // InternalDatatypes.g:2759:2: ()
            {
             before(grammarAccess.getFEnumerationTypeAccess().getFEnumerationTypeAction_0()); 
            // InternalDatatypes.g:2760:2: ()
            // InternalDatatypes.g:2760:3: 
            {
            }

             after(grammarAccess.getFEnumerationTypeAccess().getFEnumerationTypeAction_0()); 

            }


            }

        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__0__Impl"


    // $ANTLR start "rule__FEnumerationType__Group__1"
    // InternalDatatypes.g:2768:1: rule__FEnumerationType__Group__1 : rule__FEnumerationType__Group__1__Impl rule__FEnumerationType__Group__2 ;
    public final void rule__FEnumerationType__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2772:1: ( rule__FEnumerationType__Group__1__Impl rule__FEnumerationType__Group__2 )
            // InternalDatatypes.g:2773:2: rule__FEnumerationType__Group__1__Impl rule__FEnumerationType__Group__2
            {
            pushFollow(FOLLOW_36);
            rule__FEnumerationType__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__1"


    // $ANTLR start "rule__FEnumerationType__Group__1__Impl"
    // InternalDatatypes.g:2780:1: rule__FEnumerationType__Group__1__Impl : ( ( rule__FEnumerationType__CommentAssignment_1 )? ) ;
    public final void rule__FEnumerationType__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2784:1: ( ( ( rule__FEnumerationType__CommentAssignment_1 )? ) )
            // InternalDatatypes.g:2785:1: ( ( rule__FEnumerationType__CommentAssignment_1 )? )
            {
            // InternalDatatypes.g:2785:1: ( ( rule__FEnumerationType__CommentAssignment_1 )? )
            // InternalDatatypes.g:2786:2: ( rule__FEnumerationType__CommentAssignment_1 )?
            {
             before(grammarAccess.getFEnumerationTypeAccess().getCommentAssignment_1()); 
            // InternalDatatypes.g:2787:2: ( rule__FEnumerationType__CommentAssignment_1 )?
            int alt24=2;
            int LA24_0 = input.LA(1);

            if ( (LA24_0==29) ) {
                alt24=1;
            }
            switch (alt24) {
                case 1 :
                    // InternalDatatypes.g:2787:3: rule__FEnumerationType__CommentAssignment_1
                    {
                    pushFollow(FOLLOW_2);
                    rule__FEnumerationType__CommentAssignment_1();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFEnumerationTypeAccess().getCommentAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__1__Impl"


    // $ANTLR start "rule__FEnumerationType__Group__2"
    // InternalDatatypes.g:2795:1: rule__FEnumerationType__Group__2 : rule__FEnumerationType__Group__2__Impl rule__FEnumerationType__Group__3 ;
    public final void rule__FEnumerationType__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2799:1: ( rule__FEnumerationType__Group__2__Impl rule__FEnumerationType__Group__3 )
            // InternalDatatypes.g:2800:2: rule__FEnumerationType__Group__2__Impl rule__FEnumerationType__Group__3
            {
            pushFollow(FOLLOW_7);
            rule__FEnumerationType__Group__2__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group__3();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__2"


    // $ANTLR start "rule__FEnumerationType__Group__2__Impl"
    // InternalDatatypes.g:2807:1: rule__FEnumerationType__Group__2__Impl : ( 'enumeration' ) ;
    public final void rule__FEnumerationType__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2811:1: ( ( 'enumeration' ) )
            // InternalDatatypes.g:2812:1: ( 'enumeration' )
            {
            // InternalDatatypes.g:2812:1: ( 'enumeration' )
            // InternalDatatypes.g:2813:2: 'enumeration'
            {
             before(grammarAccess.getFEnumerationTypeAccess().getEnumerationKeyword_2()); 
            match(input,45,FOLLOW_2); 
             after(grammarAccess.getFEnumerationTypeAccess().getEnumerationKeyword_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__2__Impl"


    // $ANTLR start "rule__FEnumerationType__Group__3"
    // InternalDatatypes.g:2822:1: rule__FEnumerationType__Group__3 : rule__FEnumerationType__Group__3__Impl rule__FEnumerationType__Group__4 ;
    public final void rule__FEnumerationType__Group__3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2826:1: ( rule__FEnumerationType__Group__3__Impl rule__FEnumerationType__Group__4 )
            // InternalDatatypes.g:2827:2: rule__FEnumerationType__Group__3__Impl rule__FEnumerationType__Group__4
            {
            pushFollow(FOLLOW_33);
            rule__FEnumerationType__Group__3__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group__4();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__3"


    // $ANTLR start "rule__FEnumerationType__Group__3__Impl"
    // InternalDatatypes.g:2834:1: rule__FEnumerationType__Group__3__Impl : ( ( rule__FEnumerationType__NameAssignment_3 ) ) ;
    public final void rule__FEnumerationType__Group__3__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2838:1: ( ( ( rule__FEnumerationType__NameAssignment_3 ) ) )
            // InternalDatatypes.g:2839:1: ( ( rule__FEnumerationType__NameAssignment_3 ) )
            {
            // InternalDatatypes.g:2839:1: ( ( rule__FEnumerationType__NameAssignment_3 ) )
            // InternalDatatypes.g:2840:2: ( rule__FEnumerationType__NameAssignment_3 )
            {
             before(grammarAccess.getFEnumerationTypeAccess().getNameAssignment_3()); 
            // InternalDatatypes.g:2841:2: ( rule__FEnumerationType__NameAssignment_3 )
            // InternalDatatypes.g:2841:3: rule__FEnumerationType__NameAssignment_3
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerationType__NameAssignment_3();

            state._fsp--;


            }

             after(grammarAccess.getFEnumerationTypeAccess().getNameAssignment_3()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__3__Impl"


    // $ANTLR start "rule__FEnumerationType__Group__4"
    // InternalDatatypes.g:2849:1: rule__FEnumerationType__Group__4 : rule__FEnumerationType__Group__4__Impl rule__FEnumerationType__Group__5 ;
    public final void rule__FEnumerationType__Group__4() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2853:1: ( rule__FEnumerationType__Group__4__Impl rule__FEnumerationType__Group__5 )
            // InternalDatatypes.g:2854:2: rule__FEnumerationType__Group__4__Impl rule__FEnumerationType__Group__5
            {
            pushFollow(FOLLOW_33);
            rule__FEnumerationType__Group__4__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group__5();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__4"


    // $ANTLR start "rule__FEnumerationType__Group__4__Impl"
    // InternalDatatypes.g:2861:1: rule__FEnumerationType__Group__4__Impl : ( ( rule__FEnumerationType__Group_4__0 )? ) ;
    public final void rule__FEnumerationType__Group__4__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2865:1: ( ( ( rule__FEnumerationType__Group_4__0 )? ) )
            // InternalDatatypes.g:2866:1: ( ( rule__FEnumerationType__Group_4__0 )? )
            {
            // InternalDatatypes.g:2866:1: ( ( rule__FEnumerationType__Group_4__0 )? )
            // InternalDatatypes.g:2867:2: ( rule__FEnumerationType__Group_4__0 )?
            {
             before(grammarAccess.getFEnumerationTypeAccess().getGroup_4()); 
            // InternalDatatypes.g:2868:2: ( rule__FEnumerationType__Group_4__0 )?
            int alt25=2;
            int LA25_0 = input.LA(1);

            if ( (LA25_0==44) ) {
                alt25=1;
            }
            switch (alt25) {
                case 1 :
                    // InternalDatatypes.g:2868:3: rule__FEnumerationType__Group_4__0
                    {
                    pushFollow(FOLLOW_2);
                    rule__FEnumerationType__Group_4__0();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFEnumerationTypeAccess().getGroup_4()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__4__Impl"


    // $ANTLR start "rule__FEnumerationType__Group__5"
    // InternalDatatypes.g:2876:1: rule__FEnumerationType__Group__5 : rule__FEnumerationType__Group__5__Impl rule__FEnumerationType__Group__6 ;
    public final void rule__FEnumerationType__Group__5() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2880:1: ( rule__FEnumerationType__Group__5__Impl rule__FEnumerationType__Group__6 )
            // InternalDatatypes.g:2881:2: rule__FEnumerationType__Group__5__Impl rule__FEnumerationType__Group__6
            {
            pushFollow(FOLLOW_37);
            rule__FEnumerationType__Group__5__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group__6();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__5"


    // $ANTLR start "rule__FEnumerationType__Group__5__Impl"
    // InternalDatatypes.g:2888:1: rule__FEnumerationType__Group__5__Impl : ( '{' ) ;
    public final void rule__FEnumerationType__Group__5__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2892:1: ( ( '{' ) )
            // InternalDatatypes.g:2893:1: ( '{' )
            {
            // InternalDatatypes.g:2893:1: ( '{' )
            // InternalDatatypes.g:2894:2: '{'
            {
             before(grammarAccess.getFEnumerationTypeAccess().getLeftCurlyBracketKeyword_5()); 
            match(input,32,FOLLOW_2); 
             after(grammarAccess.getFEnumerationTypeAccess().getLeftCurlyBracketKeyword_5()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__5__Impl"


    // $ANTLR start "rule__FEnumerationType__Group__6"
    // InternalDatatypes.g:2903:1: rule__FEnumerationType__Group__6 : rule__FEnumerationType__Group__6__Impl rule__FEnumerationType__Group__7 ;
    public final void rule__FEnumerationType__Group__6() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2907:1: ( rule__FEnumerationType__Group__6__Impl rule__FEnumerationType__Group__7 )
            // InternalDatatypes.g:2908:2: rule__FEnumerationType__Group__6__Impl rule__FEnumerationType__Group__7
            {
            pushFollow(FOLLOW_37);
            rule__FEnumerationType__Group__6__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group__7();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__6"


    // $ANTLR start "rule__FEnumerationType__Group__6__Impl"
    // InternalDatatypes.g:2915:1: rule__FEnumerationType__Group__6__Impl : ( ( rule__FEnumerationType__Group_6__0 )? ) ;
    public final void rule__FEnumerationType__Group__6__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2919:1: ( ( ( rule__FEnumerationType__Group_6__0 )? ) )
            // InternalDatatypes.g:2920:1: ( ( rule__FEnumerationType__Group_6__0 )? )
            {
            // InternalDatatypes.g:2920:1: ( ( rule__FEnumerationType__Group_6__0 )? )
            // InternalDatatypes.g:2921:2: ( rule__FEnumerationType__Group_6__0 )?
            {
             before(grammarAccess.getFEnumerationTypeAccess().getGroup_6()); 
            // InternalDatatypes.g:2922:2: ( rule__FEnumerationType__Group_6__0 )?
            int alt26=2;
            int LA26_0 = input.LA(1);

            if ( (LA26_0==RULE_ID||LA26_0==29) ) {
                alt26=1;
            }
            switch (alt26) {
                case 1 :
                    // InternalDatatypes.g:2922:3: rule__FEnumerationType__Group_6__0
                    {
                    pushFollow(FOLLOW_2);
                    rule__FEnumerationType__Group_6__0();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFEnumerationTypeAccess().getGroup_6()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__6__Impl"


    // $ANTLR start "rule__FEnumerationType__Group__7"
    // InternalDatatypes.g:2930:1: rule__FEnumerationType__Group__7 : rule__FEnumerationType__Group__7__Impl ;
    public final void rule__FEnumerationType__Group__7() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2934:1: ( rule__FEnumerationType__Group__7__Impl )
            // InternalDatatypes.g:2935:2: rule__FEnumerationType__Group__7__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group__7__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__7"


    // $ANTLR start "rule__FEnumerationType__Group__7__Impl"
    // InternalDatatypes.g:2941:1: rule__FEnumerationType__Group__7__Impl : ( '}' ) ;
    public final void rule__FEnumerationType__Group__7__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2945:1: ( ( '}' ) )
            // InternalDatatypes.g:2946:1: ( '}' )
            {
            // InternalDatatypes.g:2946:1: ( '}' )
            // InternalDatatypes.g:2947:2: '}'
            {
             before(grammarAccess.getFEnumerationTypeAccess().getRightCurlyBracketKeyword_7()); 
            match(input,33,FOLLOW_2); 
             after(grammarAccess.getFEnumerationTypeAccess().getRightCurlyBracketKeyword_7()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group__7__Impl"


    // $ANTLR start "rule__FEnumerationType__Group_4__0"
    // InternalDatatypes.g:2957:1: rule__FEnumerationType__Group_4__0 : rule__FEnumerationType__Group_4__0__Impl rule__FEnumerationType__Group_4__1 ;
    public final void rule__FEnumerationType__Group_4__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2961:1: ( rule__FEnumerationType__Group_4__0__Impl rule__FEnumerationType__Group_4__1 )
            // InternalDatatypes.g:2962:2: rule__FEnumerationType__Group_4__0__Impl rule__FEnumerationType__Group_4__1
            {
            pushFollow(FOLLOW_7);
            rule__FEnumerationType__Group_4__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group_4__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group_4__0"


    // $ANTLR start "rule__FEnumerationType__Group_4__0__Impl"
    // InternalDatatypes.g:2969:1: rule__FEnumerationType__Group_4__0__Impl : ( 'extends' ) ;
    public final void rule__FEnumerationType__Group_4__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2973:1: ( ( 'extends' ) )
            // InternalDatatypes.g:2974:1: ( 'extends' )
            {
            // InternalDatatypes.g:2974:1: ( 'extends' )
            // InternalDatatypes.g:2975:2: 'extends'
            {
             before(grammarAccess.getFEnumerationTypeAccess().getExtendsKeyword_4_0()); 
            match(input,44,FOLLOW_2); 
             after(grammarAccess.getFEnumerationTypeAccess().getExtendsKeyword_4_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group_4__0__Impl"


    // $ANTLR start "rule__FEnumerationType__Group_4__1"
    // InternalDatatypes.g:2984:1: rule__FEnumerationType__Group_4__1 : rule__FEnumerationType__Group_4__1__Impl ;
    public final void rule__FEnumerationType__Group_4__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2988:1: ( rule__FEnumerationType__Group_4__1__Impl )
            // InternalDatatypes.g:2989:2: rule__FEnumerationType__Group_4__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group_4__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group_4__1"


    // $ANTLR start "rule__FEnumerationType__Group_4__1__Impl"
    // InternalDatatypes.g:2995:1: rule__FEnumerationType__Group_4__1__Impl : ( ( rule__FEnumerationType__BaseAssignment_4_1 ) ) ;
    public final void rule__FEnumerationType__Group_4__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:2999:1: ( ( ( rule__FEnumerationType__BaseAssignment_4_1 ) ) )
            // InternalDatatypes.g:3000:1: ( ( rule__FEnumerationType__BaseAssignment_4_1 ) )
            {
            // InternalDatatypes.g:3000:1: ( ( rule__FEnumerationType__BaseAssignment_4_1 ) )
            // InternalDatatypes.g:3001:2: ( rule__FEnumerationType__BaseAssignment_4_1 )
            {
             before(grammarAccess.getFEnumerationTypeAccess().getBaseAssignment_4_1()); 
            // InternalDatatypes.g:3002:2: ( rule__FEnumerationType__BaseAssignment_4_1 )
            // InternalDatatypes.g:3002:3: rule__FEnumerationType__BaseAssignment_4_1
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerationType__BaseAssignment_4_1();

            state._fsp--;


            }

             after(grammarAccess.getFEnumerationTypeAccess().getBaseAssignment_4_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group_4__1__Impl"


    // $ANTLR start "rule__FEnumerationType__Group_6__0"
    // InternalDatatypes.g:3011:1: rule__FEnumerationType__Group_6__0 : rule__FEnumerationType__Group_6__0__Impl rule__FEnumerationType__Group_6__1 ;
    public final void rule__FEnumerationType__Group_6__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3015:1: ( rule__FEnumerationType__Group_6__0__Impl rule__FEnumerationType__Group_6__1 )
            // InternalDatatypes.g:3016:2: rule__FEnumerationType__Group_6__0__Impl rule__FEnumerationType__Group_6__1
            {
            pushFollow(FOLLOW_38);
            rule__FEnumerationType__Group_6__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group_6__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group_6__0"


    // $ANTLR start "rule__FEnumerationType__Group_6__0__Impl"
    // InternalDatatypes.g:3023:1: rule__FEnumerationType__Group_6__0__Impl : ( ( rule__FEnumerationType__EnumeratorsAssignment_6_0 ) ) ;
    public final void rule__FEnumerationType__Group_6__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3027:1: ( ( ( rule__FEnumerationType__EnumeratorsAssignment_6_0 ) ) )
            // InternalDatatypes.g:3028:1: ( ( rule__FEnumerationType__EnumeratorsAssignment_6_0 ) )
            {
            // InternalDatatypes.g:3028:1: ( ( rule__FEnumerationType__EnumeratorsAssignment_6_0 ) )
            // InternalDatatypes.g:3029:2: ( rule__FEnumerationType__EnumeratorsAssignment_6_0 )
            {
             before(grammarAccess.getFEnumerationTypeAccess().getEnumeratorsAssignment_6_0()); 
            // InternalDatatypes.g:3030:2: ( rule__FEnumerationType__EnumeratorsAssignment_6_0 )
            // InternalDatatypes.g:3030:3: rule__FEnumerationType__EnumeratorsAssignment_6_0
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerationType__EnumeratorsAssignment_6_0();

            state._fsp--;


            }

             after(grammarAccess.getFEnumerationTypeAccess().getEnumeratorsAssignment_6_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group_6__0__Impl"


    // $ANTLR start "rule__FEnumerationType__Group_6__1"
    // InternalDatatypes.g:3038:1: rule__FEnumerationType__Group_6__1 : rule__FEnumerationType__Group_6__1__Impl ;
    public final void rule__FEnumerationType__Group_6__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3042:1: ( rule__FEnumerationType__Group_6__1__Impl )
            // InternalDatatypes.g:3043:2: rule__FEnumerationType__Group_6__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group_6__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group_6__1"


    // $ANTLR start "rule__FEnumerationType__Group_6__1__Impl"
    // InternalDatatypes.g:3049:1: rule__FEnumerationType__Group_6__1__Impl : ( ( rule__FEnumerationType__Group_6_1__0 )* ) ;
    public final void rule__FEnumerationType__Group_6__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3053:1: ( ( ( rule__FEnumerationType__Group_6_1__0 )* ) )
            // InternalDatatypes.g:3054:1: ( ( rule__FEnumerationType__Group_6_1__0 )* )
            {
            // InternalDatatypes.g:3054:1: ( ( rule__FEnumerationType__Group_6_1__0 )* )
            // InternalDatatypes.g:3055:2: ( rule__FEnumerationType__Group_6_1__0 )*
            {
             before(grammarAccess.getFEnumerationTypeAccess().getGroup_6_1()); 
            // InternalDatatypes.g:3056:2: ( rule__FEnumerationType__Group_6_1__0 )*
            loop27:
            do {
                int alt27=2;
                int LA27_0 = input.LA(1);

                if ( (LA27_0==RULE_ID||LA27_0==29||LA27_0==46) ) {
                    alt27=1;
                }


                switch (alt27) {
            	case 1 :
            	    // InternalDatatypes.g:3056:3: rule__FEnumerationType__Group_6_1__0
            	    {
            	    pushFollow(FOLLOW_39);
            	    rule__FEnumerationType__Group_6_1__0();

            	    state._fsp--;


            	    }
            	    break;

            	default :
            	    break loop27;
                }
            } while (true);

             after(grammarAccess.getFEnumerationTypeAccess().getGroup_6_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group_6__1__Impl"


    // $ANTLR start "rule__FEnumerationType__Group_6_1__0"
    // InternalDatatypes.g:3065:1: rule__FEnumerationType__Group_6_1__0 : rule__FEnumerationType__Group_6_1__0__Impl rule__FEnumerationType__Group_6_1__1 ;
    public final void rule__FEnumerationType__Group_6_1__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3069:1: ( rule__FEnumerationType__Group_6_1__0__Impl rule__FEnumerationType__Group_6_1__1 )
            // InternalDatatypes.g:3070:2: rule__FEnumerationType__Group_6_1__0__Impl rule__FEnumerationType__Group_6_1__1
            {
            pushFollow(FOLLOW_38);
            rule__FEnumerationType__Group_6_1__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group_6_1__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group_6_1__0"


    // $ANTLR start "rule__FEnumerationType__Group_6_1__0__Impl"
    // InternalDatatypes.g:3077:1: rule__FEnumerationType__Group_6_1__0__Impl : ( ( ',' )? ) ;
    public final void rule__FEnumerationType__Group_6_1__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3081:1: ( ( ( ',' )? ) )
            // InternalDatatypes.g:3082:1: ( ( ',' )? )
            {
            // InternalDatatypes.g:3082:1: ( ( ',' )? )
            // InternalDatatypes.g:3083:2: ( ',' )?
            {
             before(grammarAccess.getFEnumerationTypeAccess().getCommaKeyword_6_1_0()); 
            // InternalDatatypes.g:3084:2: ( ',' )?
            int alt28=2;
            int LA28_0 = input.LA(1);

            if ( (LA28_0==46) ) {
                alt28=1;
            }
            switch (alt28) {
                case 1 :
                    // InternalDatatypes.g:3084:3: ','
                    {
                    match(input,46,FOLLOW_2); 

                    }
                    break;

            }

             after(grammarAccess.getFEnumerationTypeAccess().getCommaKeyword_6_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group_6_1__0__Impl"


    // $ANTLR start "rule__FEnumerationType__Group_6_1__1"
    // InternalDatatypes.g:3092:1: rule__FEnumerationType__Group_6_1__1 : rule__FEnumerationType__Group_6_1__1__Impl ;
    public final void rule__FEnumerationType__Group_6_1__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3096:1: ( rule__FEnumerationType__Group_6_1__1__Impl )
            // InternalDatatypes.g:3097:2: rule__FEnumerationType__Group_6_1__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerationType__Group_6_1__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group_6_1__1"


    // $ANTLR start "rule__FEnumerationType__Group_6_1__1__Impl"
    // InternalDatatypes.g:3103:1: rule__FEnumerationType__Group_6_1__1__Impl : ( ( rule__FEnumerationType__EnumeratorsAssignment_6_1_1 ) ) ;
    public final void rule__FEnumerationType__Group_6_1__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3107:1: ( ( ( rule__FEnumerationType__EnumeratorsAssignment_6_1_1 ) ) )
            // InternalDatatypes.g:3108:1: ( ( rule__FEnumerationType__EnumeratorsAssignment_6_1_1 ) )
            {
            // InternalDatatypes.g:3108:1: ( ( rule__FEnumerationType__EnumeratorsAssignment_6_1_1 ) )
            // InternalDatatypes.g:3109:2: ( rule__FEnumerationType__EnumeratorsAssignment_6_1_1 )
            {
             before(grammarAccess.getFEnumerationTypeAccess().getEnumeratorsAssignment_6_1_1()); 
            // InternalDatatypes.g:3110:2: ( rule__FEnumerationType__EnumeratorsAssignment_6_1_1 )
            // InternalDatatypes.g:3110:3: rule__FEnumerationType__EnumeratorsAssignment_6_1_1
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerationType__EnumeratorsAssignment_6_1_1();

            state._fsp--;


            }

             after(grammarAccess.getFEnumerationTypeAccess().getEnumeratorsAssignment_6_1_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__Group_6_1__1__Impl"


    // $ANTLR start "rule__FEnumerator__Group__0"
    // InternalDatatypes.g:3119:1: rule__FEnumerator__Group__0 : rule__FEnumerator__Group__0__Impl rule__FEnumerator__Group__1 ;
    public final void rule__FEnumerator__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3123:1: ( rule__FEnumerator__Group__0__Impl rule__FEnumerator__Group__1 )
            // InternalDatatypes.g:3124:2: rule__FEnumerator__Group__0__Impl rule__FEnumerator__Group__1
            {
            pushFollow(FOLLOW_40);
            rule__FEnumerator__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerator__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__Group__0"


    // $ANTLR start "rule__FEnumerator__Group__0__Impl"
    // InternalDatatypes.g:3131:1: rule__FEnumerator__Group__0__Impl : ( () ) ;
    public final void rule__FEnumerator__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3135:1: ( ( () ) )
            // InternalDatatypes.g:3136:1: ( () )
            {
            // InternalDatatypes.g:3136:1: ( () )
            // InternalDatatypes.g:3137:2: ()
            {
             before(grammarAccess.getFEnumeratorAccess().getFEnumeratorAction_0()); 
            // InternalDatatypes.g:3138:2: ()
            // InternalDatatypes.g:3138:3: 
            {
            }

             after(grammarAccess.getFEnumeratorAccess().getFEnumeratorAction_0()); 

            }


            }

        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__Group__0__Impl"


    // $ANTLR start "rule__FEnumerator__Group__1"
    // InternalDatatypes.g:3146:1: rule__FEnumerator__Group__1 : rule__FEnumerator__Group__1__Impl rule__FEnumerator__Group__2 ;
    public final void rule__FEnumerator__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3150:1: ( rule__FEnumerator__Group__1__Impl rule__FEnumerator__Group__2 )
            // InternalDatatypes.g:3151:2: rule__FEnumerator__Group__1__Impl rule__FEnumerator__Group__2
            {
            pushFollow(FOLLOW_40);
            rule__FEnumerator__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerator__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__Group__1"


    // $ANTLR start "rule__FEnumerator__Group__1__Impl"
    // InternalDatatypes.g:3158:1: rule__FEnumerator__Group__1__Impl : ( ( rule__FEnumerator__CommentAssignment_1 )? ) ;
    public final void rule__FEnumerator__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3162:1: ( ( ( rule__FEnumerator__CommentAssignment_1 )? ) )
            // InternalDatatypes.g:3163:1: ( ( rule__FEnumerator__CommentAssignment_1 )? )
            {
            // InternalDatatypes.g:3163:1: ( ( rule__FEnumerator__CommentAssignment_1 )? )
            // InternalDatatypes.g:3164:2: ( rule__FEnumerator__CommentAssignment_1 )?
            {
             before(grammarAccess.getFEnumeratorAccess().getCommentAssignment_1()); 
            // InternalDatatypes.g:3165:2: ( rule__FEnumerator__CommentAssignment_1 )?
            int alt29=2;
            int LA29_0 = input.LA(1);

            if ( (LA29_0==29) ) {
                alt29=1;
            }
            switch (alt29) {
                case 1 :
                    // InternalDatatypes.g:3165:3: rule__FEnumerator__CommentAssignment_1
                    {
                    pushFollow(FOLLOW_2);
                    rule__FEnumerator__CommentAssignment_1();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFEnumeratorAccess().getCommentAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__Group__1__Impl"


    // $ANTLR start "rule__FEnumerator__Group__2"
    // InternalDatatypes.g:3173:1: rule__FEnumerator__Group__2 : rule__FEnumerator__Group__2__Impl rule__FEnumerator__Group__3 ;
    public final void rule__FEnumerator__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3177:1: ( rule__FEnumerator__Group__2__Impl rule__FEnumerator__Group__3 )
            // InternalDatatypes.g:3178:2: rule__FEnumerator__Group__2__Impl rule__FEnumerator__Group__3
            {
            pushFollow(FOLLOW_41);
            rule__FEnumerator__Group__2__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerator__Group__3();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__Group__2"


    // $ANTLR start "rule__FEnumerator__Group__2__Impl"
    // InternalDatatypes.g:3185:1: rule__FEnumerator__Group__2__Impl : ( ( rule__FEnumerator__NameAssignment_2 ) ) ;
    public final void rule__FEnumerator__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3189:1: ( ( ( rule__FEnumerator__NameAssignment_2 ) ) )
            // InternalDatatypes.g:3190:1: ( ( rule__FEnumerator__NameAssignment_2 ) )
            {
            // InternalDatatypes.g:3190:1: ( ( rule__FEnumerator__NameAssignment_2 ) )
            // InternalDatatypes.g:3191:2: ( rule__FEnumerator__NameAssignment_2 )
            {
             before(grammarAccess.getFEnumeratorAccess().getNameAssignment_2()); 
            // InternalDatatypes.g:3192:2: ( rule__FEnumerator__NameAssignment_2 )
            // InternalDatatypes.g:3192:3: rule__FEnumerator__NameAssignment_2
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerator__NameAssignment_2();

            state._fsp--;


            }

             after(grammarAccess.getFEnumeratorAccess().getNameAssignment_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__Group__2__Impl"


    // $ANTLR start "rule__FEnumerator__Group__3"
    // InternalDatatypes.g:3200:1: rule__FEnumerator__Group__3 : rule__FEnumerator__Group__3__Impl ;
    public final void rule__FEnumerator__Group__3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3204:1: ( rule__FEnumerator__Group__3__Impl )
            // InternalDatatypes.g:3205:2: rule__FEnumerator__Group__3__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerator__Group__3__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__Group__3"


    // $ANTLR start "rule__FEnumerator__Group__3__Impl"
    // InternalDatatypes.g:3211:1: rule__FEnumerator__Group__3__Impl : ( ( rule__FEnumerator__Group_3__0 )? ) ;
    public final void rule__FEnumerator__Group__3__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3215:1: ( ( ( rule__FEnumerator__Group_3__0 )? ) )
            // InternalDatatypes.g:3216:1: ( ( rule__FEnumerator__Group_3__0 )? )
            {
            // InternalDatatypes.g:3216:1: ( ( rule__FEnumerator__Group_3__0 )? )
            // InternalDatatypes.g:3217:2: ( rule__FEnumerator__Group_3__0 )?
            {
             before(grammarAccess.getFEnumeratorAccess().getGroup_3()); 
            // InternalDatatypes.g:3218:2: ( rule__FEnumerator__Group_3__0 )?
            int alt30=2;
            int LA30_0 = input.LA(1);

            if ( (LA30_0==47) ) {
                alt30=1;
            }
            switch (alt30) {
                case 1 :
                    // InternalDatatypes.g:3218:3: rule__FEnumerator__Group_3__0
                    {
                    pushFollow(FOLLOW_2);
                    rule__FEnumerator__Group_3__0();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFEnumeratorAccess().getGroup_3()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__Group__3__Impl"


    // $ANTLR start "rule__FEnumerator__Group_3__0"
    // InternalDatatypes.g:3227:1: rule__FEnumerator__Group_3__0 : rule__FEnumerator__Group_3__0__Impl rule__FEnumerator__Group_3__1 ;
    public final void rule__FEnumerator__Group_3__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3231:1: ( rule__FEnumerator__Group_3__0__Impl rule__FEnumerator__Group_3__1 )
            // InternalDatatypes.g:3232:2: rule__FEnumerator__Group_3__0__Impl rule__FEnumerator__Group_3__1
            {
            pushFollow(FOLLOW_42);
            rule__FEnumerator__Group_3__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FEnumerator__Group_3__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__Group_3__0"


    // $ANTLR start "rule__FEnumerator__Group_3__0__Impl"
    // InternalDatatypes.g:3239:1: rule__FEnumerator__Group_3__0__Impl : ( '=' ) ;
    public final void rule__FEnumerator__Group_3__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3243:1: ( ( '=' ) )
            // InternalDatatypes.g:3244:1: ( '=' )
            {
            // InternalDatatypes.g:3244:1: ( '=' )
            // InternalDatatypes.g:3245:2: '='
            {
             before(grammarAccess.getFEnumeratorAccess().getEqualsSignKeyword_3_0()); 
            match(input,47,FOLLOW_2); 
             after(grammarAccess.getFEnumeratorAccess().getEqualsSignKeyword_3_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__Group_3__0__Impl"


    // $ANTLR start "rule__FEnumerator__Group_3__1"
    // InternalDatatypes.g:3254:1: rule__FEnumerator__Group_3__1 : rule__FEnumerator__Group_3__1__Impl ;
    public final void rule__FEnumerator__Group_3__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3258:1: ( rule__FEnumerator__Group_3__1__Impl )
            // InternalDatatypes.g:3259:2: rule__FEnumerator__Group_3__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerator__Group_3__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__Group_3__1"


    // $ANTLR start "rule__FEnumerator__Group_3__1__Impl"
    // InternalDatatypes.g:3265:1: rule__FEnumerator__Group_3__1__Impl : ( ( rule__FEnumerator__ValueAssignment_3_1 ) ) ;
    public final void rule__FEnumerator__Group_3__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3269:1: ( ( ( rule__FEnumerator__ValueAssignment_3_1 ) ) )
            // InternalDatatypes.g:3270:1: ( ( rule__FEnumerator__ValueAssignment_3_1 ) )
            {
            // InternalDatatypes.g:3270:1: ( ( rule__FEnumerator__ValueAssignment_3_1 ) )
            // InternalDatatypes.g:3271:2: ( rule__FEnumerator__ValueAssignment_3_1 )
            {
             before(grammarAccess.getFEnumeratorAccess().getValueAssignment_3_1()); 
            // InternalDatatypes.g:3272:2: ( rule__FEnumerator__ValueAssignment_3_1 )
            // InternalDatatypes.g:3272:3: rule__FEnumerator__ValueAssignment_3_1
            {
            pushFollow(FOLLOW_2);
            rule__FEnumerator__ValueAssignment_3_1();

            state._fsp--;


            }

             after(grammarAccess.getFEnumeratorAccess().getValueAssignment_3_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__Group_3__1__Impl"


    // $ANTLR start "rule__FMapType__Group__0"
    // InternalDatatypes.g:3281:1: rule__FMapType__Group__0 : rule__FMapType__Group__0__Impl rule__FMapType__Group__1 ;
    public final void rule__FMapType__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3285:1: ( rule__FMapType__Group__0__Impl rule__FMapType__Group__1 )
            // InternalDatatypes.g:3286:2: rule__FMapType__Group__0__Impl rule__FMapType__Group__1
            {
            pushFollow(FOLLOW_43);
            rule__FMapType__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMapType__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__0"


    // $ANTLR start "rule__FMapType__Group__0__Impl"
    // InternalDatatypes.g:3293:1: rule__FMapType__Group__0__Impl : ( () ) ;
    public final void rule__FMapType__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3297:1: ( ( () ) )
            // InternalDatatypes.g:3298:1: ( () )
            {
            // InternalDatatypes.g:3298:1: ( () )
            // InternalDatatypes.g:3299:2: ()
            {
             before(grammarAccess.getFMapTypeAccess().getFMapTypeAction_0()); 
            // InternalDatatypes.g:3300:2: ()
            // InternalDatatypes.g:3300:3: 
            {
            }

             after(grammarAccess.getFMapTypeAccess().getFMapTypeAction_0()); 

            }


            }

        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__0__Impl"


    // $ANTLR start "rule__FMapType__Group__1"
    // InternalDatatypes.g:3308:1: rule__FMapType__Group__1 : rule__FMapType__Group__1__Impl rule__FMapType__Group__2 ;
    public final void rule__FMapType__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3312:1: ( rule__FMapType__Group__1__Impl rule__FMapType__Group__2 )
            // InternalDatatypes.g:3313:2: rule__FMapType__Group__1__Impl rule__FMapType__Group__2
            {
            pushFollow(FOLLOW_43);
            rule__FMapType__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMapType__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__1"


    // $ANTLR start "rule__FMapType__Group__1__Impl"
    // InternalDatatypes.g:3320:1: rule__FMapType__Group__1__Impl : ( ( rule__FMapType__CommentAssignment_1 )? ) ;
    public final void rule__FMapType__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3324:1: ( ( ( rule__FMapType__CommentAssignment_1 )? ) )
            // InternalDatatypes.g:3325:1: ( ( rule__FMapType__CommentAssignment_1 )? )
            {
            // InternalDatatypes.g:3325:1: ( ( rule__FMapType__CommentAssignment_1 )? )
            // InternalDatatypes.g:3326:2: ( rule__FMapType__CommentAssignment_1 )?
            {
             before(grammarAccess.getFMapTypeAccess().getCommentAssignment_1()); 
            // InternalDatatypes.g:3327:2: ( rule__FMapType__CommentAssignment_1 )?
            int alt31=2;
            int LA31_0 = input.LA(1);

            if ( (LA31_0==29) ) {
                alt31=1;
            }
            switch (alt31) {
                case 1 :
                    // InternalDatatypes.g:3327:3: rule__FMapType__CommentAssignment_1
                    {
                    pushFollow(FOLLOW_2);
                    rule__FMapType__CommentAssignment_1();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFMapTypeAccess().getCommentAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__1__Impl"


    // $ANTLR start "rule__FMapType__Group__2"
    // InternalDatatypes.g:3335:1: rule__FMapType__Group__2 : rule__FMapType__Group__2__Impl rule__FMapType__Group__3 ;
    public final void rule__FMapType__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3339:1: ( rule__FMapType__Group__2__Impl rule__FMapType__Group__3 )
            // InternalDatatypes.g:3340:2: rule__FMapType__Group__2__Impl rule__FMapType__Group__3
            {
            pushFollow(FOLLOW_7);
            rule__FMapType__Group__2__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMapType__Group__3();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__2"


    // $ANTLR start "rule__FMapType__Group__2__Impl"
    // InternalDatatypes.g:3347:1: rule__FMapType__Group__2__Impl : ( 'map' ) ;
    public final void rule__FMapType__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3351:1: ( ( 'map' ) )
            // InternalDatatypes.g:3352:1: ( 'map' )
            {
            // InternalDatatypes.g:3352:1: ( 'map' )
            // InternalDatatypes.g:3353:2: 'map'
            {
             before(grammarAccess.getFMapTypeAccess().getMapKeyword_2()); 
            match(input,48,FOLLOW_2); 
             after(grammarAccess.getFMapTypeAccess().getMapKeyword_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__2__Impl"


    // $ANTLR start "rule__FMapType__Group__3"
    // InternalDatatypes.g:3362:1: rule__FMapType__Group__3 : rule__FMapType__Group__3__Impl rule__FMapType__Group__4 ;
    public final void rule__FMapType__Group__3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3366:1: ( rule__FMapType__Group__3__Impl rule__FMapType__Group__4 )
            // InternalDatatypes.g:3367:2: rule__FMapType__Group__3__Impl rule__FMapType__Group__4
            {
            pushFollow(FOLLOW_18);
            rule__FMapType__Group__3__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMapType__Group__4();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__3"


    // $ANTLR start "rule__FMapType__Group__3__Impl"
    // InternalDatatypes.g:3374:1: rule__FMapType__Group__3__Impl : ( ( rule__FMapType__NameAssignment_3 ) ) ;
    public final void rule__FMapType__Group__3__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3378:1: ( ( ( rule__FMapType__NameAssignment_3 ) ) )
            // InternalDatatypes.g:3379:1: ( ( rule__FMapType__NameAssignment_3 ) )
            {
            // InternalDatatypes.g:3379:1: ( ( rule__FMapType__NameAssignment_3 ) )
            // InternalDatatypes.g:3380:2: ( rule__FMapType__NameAssignment_3 )
            {
             before(grammarAccess.getFMapTypeAccess().getNameAssignment_3()); 
            // InternalDatatypes.g:3381:2: ( rule__FMapType__NameAssignment_3 )
            // InternalDatatypes.g:3381:3: rule__FMapType__NameAssignment_3
            {
            pushFollow(FOLLOW_2);
            rule__FMapType__NameAssignment_3();

            state._fsp--;


            }

             after(grammarAccess.getFMapTypeAccess().getNameAssignment_3()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__3__Impl"


    // $ANTLR start "rule__FMapType__Group__4"
    // InternalDatatypes.g:3389:1: rule__FMapType__Group__4 : rule__FMapType__Group__4__Impl rule__FMapType__Group__5 ;
    public final void rule__FMapType__Group__4() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3393:1: ( rule__FMapType__Group__4__Impl rule__FMapType__Group__5 )
            // InternalDatatypes.g:3394:2: rule__FMapType__Group__4__Impl rule__FMapType__Group__5
            {
            pushFollow(FOLLOW_29);
            rule__FMapType__Group__4__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMapType__Group__5();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__4"


    // $ANTLR start "rule__FMapType__Group__4__Impl"
    // InternalDatatypes.g:3401:1: rule__FMapType__Group__4__Impl : ( '{' ) ;
    public final void rule__FMapType__Group__4__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3405:1: ( ( '{' ) )
            // InternalDatatypes.g:3406:1: ( '{' )
            {
            // InternalDatatypes.g:3406:1: ( '{' )
            // InternalDatatypes.g:3407:2: '{'
            {
             before(grammarAccess.getFMapTypeAccess().getLeftCurlyBracketKeyword_4()); 
            match(input,32,FOLLOW_2); 
             after(grammarAccess.getFMapTypeAccess().getLeftCurlyBracketKeyword_4()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__4__Impl"


    // $ANTLR start "rule__FMapType__Group__5"
    // InternalDatatypes.g:3416:1: rule__FMapType__Group__5 : rule__FMapType__Group__5__Impl rule__FMapType__Group__6 ;
    public final void rule__FMapType__Group__5() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3420:1: ( rule__FMapType__Group__5__Impl rule__FMapType__Group__6 )
            // InternalDatatypes.g:3421:2: rule__FMapType__Group__5__Impl rule__FMapType__Group__6
            {
            pushFollow(FOLLOW_44);
            rule__FMapType__Group__5__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMapType__Group__6();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__5"


    // $ANTLR start "rule__FMapType__Group__5__Impl"
    // InternalDatatypes.g:3428:1: rule__FMapType__Group__5__Impl : ( ( rule__FMapType__KeyTypeAssignment_5 ) ) ;
    public final void rule__FMapType__Group__5__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3432:1: ( ( ( rule__FMapType__KeyTypeAssignment_5 ) ) )
            // InternalDatatypes.g:3433:1: ( ( rule__FMapType__KeyTypeAssignment_5 ) )
            {
            // InternalDatatypes.g:3433:1: ( ( rule__FMapType__KeyTypeAssignment_5 ) )
            // InternalDatatypes.g:3434:2: ( rule__FMapType__KeyTypeAssignment_5 )
            {
             before(grammarAccess.getFMapTypeAccess().getKeyTypeAssignment_5()); 
            // InternalDatatypes.g:3435:2: ( rule__FMapType__KeyTypeAssignment_5 )
            // InternalDatatypes.g:3435:3: rule__FMapType__KeyTypeAssignment_5
            {
            pushFollow(FOLLOW_2);
            rule__FMapType__KeyTypeAssignment_5();

            state._fsp--;


            }

             after(grammarAccess.getFMapTypeAccess().getKeyTypeAssignment_5()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__5__Impl"


    // $ANTLR start "rule__FMapType__Group__6"
    // InternalDatatypes.g:3443:1: rule__FMapType__Group__6 : rule__FMapType__Group__6__Impl rule__FMapType__Group__7 ;
    public final void rule__FMapType__Group__6() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3447:1: ( rule__FMapType__Group__6__Impl rule__FMapType__Group__7 )
            // InternalDatatypes.g:3448:2: rule__FMapType__Group__6__Impl rule__FMapType__Group__7
            {
            pushFollow(FOLLOW_29);
            rule__FMapType__Group__6__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMapType__Group__7();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__6"


    // $ANTLR start "rule__FMapType__Group__6__Impl"
    // InternalDatatypes.g:3455:1: rule__FMapType__Group__6__Impl : ( 'to' ) ;
    public final void rule__FMapType__Group__6__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3459:1: ( ( 'to' ) )
            // InternalDatatypes.g:3460:1: ( 'to' )
            {
            // InternalDatatypes.g:3460:1: ( 'to' )
            // InternalDatatypes.g:3461:2: 'to'
            {
             before(grammarAccess.getFMapTypeAccess().getToKeyword_6()); 
            match(input,49,FOLLOW_2); 
             after(grammarAccess.getFMapTypeAccess().getToKeyword_6()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__6__Impl"


    // $ANTLR start "rule__FMapType__Group__7"
    // InternalDatatypes.g:3470:1: rule__FMapType__Group__7 : rule__FMapType__Group__7__Impl rule__FMapType__Group__8 ;
    public final void rule__FMapType__Group__7() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3474:1: ( rule__FMapType__Group__7__Impl rule__FMapType__Group__8 )
            // InternalDatatypes.g:3475:2: rule__FMapType__Group__7__Impl rule__FMapType__Group__8
            {
            pushFollow(FOLLOW_26);
            rule__FMapType__Group__7__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FMapType__Group__8();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__7"


    // $ANTLR start "rule__FMapType__Group__7__Impl"
    // InternalDatatypes.g:3482:1: rule__FMapType__Group__7__Impl : ( ( rule__FMapType__ValueTypeAssignment_7 ) ) ;
    public final void rule__FMapType__Group__7__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3486:1: ( ( ( rule__FMapType__ValueTypeAssignment_7 ) ) )
            // InternalDatatypes.g:3487:1: ( ( rule__FMapType__ValueTypeAssignment_7 ) )
            {
            // InternalDatatypes.g:3487:1: ( ( rule__FMapType__ValueTypeAssignment_7 ) )
            // InternalDatatypes.g:3488:2: ( rule__FMapType__ValueTypeAssignment_7 )
            {
             before(grammarAccess.getFMapTypeAccess().getValueTypeAssignment_7()); 
            // InternalDatatypes.g:3489:2: ( rule__FMapType__ValueTypeAssignment_7 )
            // InternalDatatypes.g:3489:3: rule__FMapType__ValueTypeAssignment_7
            {
            pushFollow(FOLLOW_2);
            rule__FMapType__ValueTypeAssignment_7();

            state._fsp--;


            }

             after(grammarAccess.getFMapTypeAccess().getValueTypeAssignment_7()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__7__Impl"


    // $ANTLR start "rule__FMapType__Group__8"
    // InternalDatatypes.g:3497:1: rule__FMapType__Group__8 : rule__FMapType__Group__8__Impl ;
    public final void rule__FMapType__Group__8() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3501:1: ( rule__FMapType__Group__8__Impl )
            // InternalDatatypes.g:3502:2: rule__FMapType__Group__8__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FMapType__Group__8__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__8"


    // $ANTLR start "rule__FMapType__Group__8__Impl"
    // InternalDatatypes.g:3508:1: rule__FMapType__Group__8__Impl : ( '}' ) ;
    public final void rule__FMapType__Group__8__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3512:1: ( ( '}' ) )
            // InternalDatatypes.g:3513:1: ( '}' )
            {
            // InternalDatatypes.g:3513:1: ( '}' )
            // InternalDatatypes.g:3514:2: '}'
            {
             before(grammarAccess.getFMapTypeAccess().getRightCurlyBracketKeyword_8()); 
            match(input,33,FOLLOW_2); 
             after(grammarAccess.getFMapTypeAccess().getRightCurlyBracketKeyword_8()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__Group__8__Impl"


    // $ANTLR start "rule__FField__Group__0"
    // InternalDatatypes.g:3524:1: rule__FField__Group__0 : rule__FField__Group__0__Impl rule__FField__Group__1 ;
    public final void rule__FField__Group__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3528:1: ( rule__FField__Group__0__Impl rule__FField__Group__1 )
            // InternalDatatypes.g:3529:2: rule__FField__Group__0__Impl rule__FField__Group__1
            {
            pushFollow(FOLLOW_45);
            rule__FField__Group__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FField__Group__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__Group__0"


    // $ANTLR start "rule__FField__Group__0__Impl"
    // InternalDatatypes.g:3536:1: rule__FField__Group__0__Impl : ( ( rule__FField__CommentAssignment_0 )? ) ;
    public final void rule__FField__Group__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3540:1: ( ( ( rule__FField__CommentAssignment_0 )? ) )
            // InternalDatatypes.g:3541:1: ( ( rule__FField__CommentAssignment_0 )? )
            {
            // InternalDatatypes.g:3541:1: ( ( rule__FField__CommentAssignment_0 )? )
            // InternalDatatypes.g:3542:2: ( rule__FField__CommentAssignment_0 )?
            {
             before(grammarAccess.getFFieldAccess().getCommentAssignment_0()); 
            // InternalDatatypes.g:3543:2: ( rule__FField__CommentAssignment_0 )?
            int alt32=2;
            int LA32_0 = input.LA(1);

            if ( (LA32_0==29) ) {
                alt32=1;
            }
            switch (alt32) {
                case 1 :
                    // InternalDatatypes.g:3543:3: rule__FField__CommentAssignment_0
                    {
                    pushFollow(FOLLOW_2);
                    rule__FField__CommentAssignment_0();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFFieldAccess().getCommentAssignment_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__Group__0__Impl"


    // $ANTLR start "rule__FField__Group__1"
    // InternalDatatypes.g:3551:1: rule__FField__Group__1 : rule__FField__Group__1__Impl rule__FField__Group__2 ;
    public final void rule__FField__Group__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3555:1: ( rule__FField__Group__1__Impl rule__FField__Group__2 )
            // InternalDatatypes.g:3556:2: rule__FField__Group__1__Impl rule__FField__Group__2
            {
            pushFollow(FOLLOW_46);
            rule__FField__Group__1__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FField__Group__2();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__Group__1"


    // $ANTLR start "rule__FField__Group__1__Impl"
    // InternalDatatypes.g:3563:1: rule__FField__Group__1__Impl : ( ( rule__FField__TypeAssignment_1 ) ) ;
    public final void rule__FField__Group__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3567:1: ( ( ( rule__FField__TypeAssignment_1 ) ) )
            // InternalDatatypes.g:3568:1: ( ( rule__FField__TypeAssignment_1 ) )
            {
            // InternalDatatypes.g:3568:1: ( ( rule__FField__TypeAssignment_1 ) )
            // InternalDatatypes.g:3569:2: ( rule__FField__TypeAssignment_1 )
            {
             before(grammarAccess.getFFieldAccess().getTypeAssignment_1()); 
            // InternalDatatypes.g:3570:2: ( rule__FField__TypeAssignment_1 )
            // InternalDatatypes.g:3570:3: rule__FField__TypeAssignment_1
            {
            pushFollow(FOLLOW_2);
            rule__FField__TypeAssignment_1();

            state._fsp--;


            }

             after(grammarAccess.getFFieldAccess().getTypeAssignment_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__Group__1__Impl"


    // $ANTLR start "rule__FField__Group__2"
    // InternalDatatypes.g:3578:1: rule__FField__Group__2 : rule__FField__Group__2__Impl rule__FField__Group__3 ;
    public final void rule__FField__Group__2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3582:1: ( rule__FField__Group__2__Impl rule__FField__Group__3 )
            // InternalDatatypes.g:3583:2: rule__FField__Group__2__Impl rule__FField__Group__3
            {
            pushFollow(FOLLOW_46);
            rule__FField__Group__2__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FField__Group__3();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__Group__2"


    // $ANTLR start "rule__FField__Group__2__Impl"
    // InternalDatatypes.g:3590:1: rule__FField__Group__2__Impl : ( ( rule__FField__Group_2__0 )? ) ;
    public final void rule__FField__Group__2__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3594:1: ( ( ( rule__FField__Group_2__0 )? ) )
            // InternalDatatypes.g:3595:1: ( ( rule__FField__Group_2__0 )? )
            {
            // InternalDatatypes.g:3595:1: ( ( rule__FField__Group_2__0 )? )
            // InternalDatatypes.g:3596:2: ( rule__FField__Group_2__0 )?
            {
             before(grammarAccess.getFFieldAccess().getGroup_2()); 
            // InternalDatatypes.g:3597:2: ( rule__FField__Group_2__0 )?
            int alt33=2;
            int LA33_0 = input.LA(1);

            if ( (LA33_0==51) ) {
                alt33=1;
            }
            switch (alt33) {
                case 1 :
                    // InternalDatatypes.g:3597:3: rule__FField__Group_2__0
                    {
                    pushFollow(FOLLOW_2);
                    rule__FField__Group_2__0();

                    state._fsp--;


                    }
                    break;

            }

             after(grammarAccess.getFFieldAccess().getGroup_2()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__Group__2__Impl"


    // $ANTLR start "rule__FField__Group__3"
    // InternalDatatypes.g:3605:1: rule__FField__Group__3 : rule__FField__Group__3__Impl ;
    public final void rule__FField__Group__3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3609:1: ( rule__FField__Group__3__Impl )
            // InternalDatatypes.g:3610:2: rule__FField__Group__3__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FField__Group__3__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__Group__3"


    // $ANTLR start "rule__FField__Group__3__Impl"
    // InternalDatatypes.g:3616:1: rule__FField__Group__3__Impl : ( ( rule__FField__NameAssignment_3 ) ) ;
    public final void rule__FField__Group__3__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3620:1: ( ( ( rule__FField__NameAssignment_3 ) ) )
            // InternalDatatypes.g:3621:1: ( ( rule__FField__NameAssignment_3 ) )
            {
            // InternalDatatypes.g:3621:1: ( ( rule__FField__NameAssignment_3 ) )
            // InternalDatatypes.g:3622:2: ( rule__FField__NameAssignment_3 )
            {
             before(grammarAccess.getFFieldAccess().getNameAssignment_3()); 
            // InternalDatatypes.g:3623:2: ( rule__FField__NameAssignment_3 )
            // InternalDatatypes.g:3623:3: rule__FField__NameAssignment_3
            {
            pushFollow(FOLLOW_2);
            rule__FField__NameAssignment_3();

            state._fsp--;


            }

             after(grammarAccess.getFFieldAccess().getNameAssignment_3()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__Group__3__Impl"


    // $ANTLR start "rule__FField__Group_2__0"
    // InternalDatatypes.g:3632:1: rule__FField__Group_2__0 : rule__FField__Group_2__0__Impl rule__FField__Group_2__1 ;
    public final void rule__FField__Group_2__0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3636:1: ( rule__FField__Group_2__0__Impl rule__FField__Group_2__1 )
            // InternalDatatypes.g:3637:2: rule__FField__Group_2__0__Impl rule__FField__Group_2__1
            {
            pushFollow(FOLLOW_47);
            rule__FField__Group_2__0__Impl();

            state._fsp--;

            pushFollow(FOLLOW_2);
            rule__FField__Group_2__1();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__Group_2__0"


    // $ANTLR start "rule__FField__Group_2__0__Impl"
    // InternalDatatypes.g:3644:1: rule__FField__Group_2__0__Impl : ( ( rule__FField__ArrayAssignment_2_0 ) ) ;
    public final void rule__FField__Group_2__0__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3648:1: ( ( ( rule__FField__ArrayAssignment_2_0 ) ) )
            // InternalDatatypes.g:3649:1: ( ( rule__FField__ArrayAssignment_2_0 ) )
            {
            // InternalDatatypes.g:3649:1: ( ( rule__FField__ArrayAssignment_2_0 ) )
            // InternalDatatypes.g:3650:2: ( rule__FField__ArrayAssignment_2_0 )
            {
             before(grammarAccess.getFFieldAccess().getArrayAssignment_2_0()); 
            // InternalDatatypes.g:3651:2: ( rule__FField__ArrayAssignment_2_0 )
            // InternalDatatypes.g:3651:3: rule__FField__ArrayAssignment_2_0
            {
            pushFollow(FOLLOW_2);
            rule__FField__ArrayAssignment_2_0();

            state._fsp--;


            }

             after(grammarAccess.getFFieldAccess().getArrayAssignment_2_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__Group_2__0__Impl"


    // $ANTLR start "rule__FField__Group_2__1"
    // InternalDatatypes.g:3659:1: rule__FField__Group_2__1 : rule__FField__Group_2__1__Impl ;
    public final void rule__FField__Group_2__1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3663:1: ( rule__FField__Group_2__1__Impl )
            // InternalDatatypes.g:3664:2: rule__FField__Group_2__1__Impl
            {
            pushFollow(FOLLOW_2);
            rule__FField__Group_2__1__Impl();

            state._fsp--;


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__Group_2__1"


    // $ANTLR start "rule__FField__Group_2__1__Impl"
    // InternalDatatypes.g:3670:1: rule__FField__Group_2__1__Impl : ( ']' ) ;
    public final void rule__FField__Group_2__1__Impl() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3674:1: ( ( ']' ) )
            // InternalDatatypes.g:3675:1: ( ']' )
            {
            // InternalDatatypes.g:3675:1: ( ']' )
            // InternalDatatypes.g:3676:2: ']'
            {
             before(grammarAccess.getFFieldAccess().getRightSquareBracketKeyword_2_1()); 
            match(input,50,FOLLOW_2); 
             after(grammarAccess.getFFieldAccess().getRightSquareBracketKeyword_2_1()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__Group_2__1__Impl"


    // $ANTLR start "rule__Model__PackAssignment_1"
    // InternalDatatypes.g:3686:1: rule__Model__PackAssignment_1 : ( rulePackage ) ;
    public final void rule__Model__PackAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3690:1: ( ( rulePackage ) )
            // InternalDatatypes.g:3691:2: ( rulePackage )
            {
            // InternalDatatypes.g:3691:2: ( rulePackage )
            // InternalDatatypes.g:3692:3: rulePackage
            {
             before(grammarAccess.getModelAccess().getPackPackageParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            rulePackage();

            state._fsp--;

             after(grammarAccess.getModelAccess().getPackPackageParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__PackAssignment_1"


    // $ANTLR start "rule__Model__ImportsAssignment_2"
    // InternalDatatypes.g:3701:1: rule__Model__ImportsAssignment_2 : ( ruleImport ) ;
    public final void rule__Model__ImportsAssignment_2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3705:1: ( ( ruleImport ) )
            // InternalDatatypes.g:3706:2: ( ruleImport )
            {
            // InternalDatatypes.g:3706:2: ( ruleImport )
            // InternalDatatypes.g:3707:3: ruleImport
            {
             before(grammarAccess.getModelAccess().getImportsImportParserRuleCall_2_0()); 
            pushFollow(FOLLOW_2);
            ruleImport();

            state._fsp--;

             after(grammarAccess.getModelAccess().getImportsImportParserRuleCall_2_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__ImportsAssignment_2"


    // $ANTLR start "rule__Model__TypeCollectionsAssignment_3_0"
    // InternalDatatypes.g:3716:1: rule__Model__TypeCollectionsAssignment_3_0 : ( ruleFTypeCollection ) ;
    public final void rule__Model__TypeCollectionsAssignment_3_0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3720:1: ( ( ruleFTypeCollection ) )
            // InternalDatatypes.g:3721:2: ( ruleFTypeCollection )
            {
            // InternalDatatypes.g:3721:2: ( ruleFTypeCollection )
            // InternalDatatypes.g:3722:3: ruleFTypeCollection
            {
             before(grammarAccess.getModelAccess().getTypeCollectionsFTypeCollectionParserRuleCall_3_0_0()); 
            pushFollow(FOLLOW_2);
            ruleFTypeCollection();

            state._fsp--;

             after(grammarAccess.getModelAccess().getTypeCollectionsFTypeCollectionParserRuleCall_3_0_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__TypeCollectionsAssignment_3_0"


    // $ANTLR start "rule__Model__MessageCollectionsAssignment_3_1"
    // InternalDatatypes.g:3731:1: rule__Model__MessageCollectionsAssignment_3_1 : ( ruleFMessageCollection ) ;
    public final void rule__Model__MessageCollectionsAssignment_3_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3735:1: ( ( ruleFMessageCollection ) )
            // InternalDatatypes.g:3736:2: ( ruleFMessageCollection )
            {
            // InternalDatatypes.g:3736:2: ( ruleFMessageCollection )
            // InternalDatatypes.g:3737:3: ruleFMessageCollection
            {
             before(grammarAccess.getModelAccess().getMessageCollectionsFMessageCollectionParserRuleCall_3_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFMessageCollection();

            state._fsp--;

             after(grammarAccess.getModelAccess().getMessageCollectionsFMessageCollectionParserRuleCall_3_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Model__MessageCollectionsAssignment_3_1"


    // $ANTLR start "rule__Package__NameAssignment_1"
    // InternalDatatypes.g:3746:1: rule__Package__NameAssignment_1 : ( ruleFQN ) ;
    public final void rule__Package__NameAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3750:1: ( ( ruleFQN ) )
            // InternalDatatypes.g:3751:2: ( ruleFQN )
            {
            // InternalDatatypes.g:3751:2: ( ruleFQN )
            // InternalDatatypes.g:3752:3: ruleFQN
            {
             before(grammarAccess.getPackageAccess().getNameFQNParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFQN();

            state._fsp--;

             after(grammarAccess.getPackageAccess().getNameFQNParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Package__NameAssignment_1"


    // $ANTLR start "rule__Import__ImportedNamespaceAssignment_1"
    // InternalDatatypes.g:3761:1: rule__Import__ImportedNamespaceAssignment_1 : ( ruleImportedFQN ) ;
    public final void rule__Import__ImportedNamespaceAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3765:1: ( ( ruleImportedFQN ) )
            // InternalDatatypes.g:3766:2: ( ruleImportedFQN )
            {
            // InternalDatatypes.g:3766:2: ( ruleImportedFQN )
            // InternalDatatypes.g:3767:3: ruleImportedFQN
            {
             before(grammarAccess.getImportAccess().getImportedNamespaceImportedFQNParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            ruleImportedFQN();

            state._fsp--;

             after(grammarAccess.getImportAccess().getImportedNamespaceImportedFQNParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__Import__ImportedNamespaceAssignment_1"


    // $ANTLR start "rule__FAnnotationBlock__ElementsAssignment_1"
    // InternalDatatypes.g:3776:1: rule__FAnnotationBlock__ElementsAssignment_1 : ( ruleFAnnotation ) ;
    public final void rule__FAnnotationBlock__ElementsAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3780:1: ( ( ruleFAnnotation ) )
            // InternalDatatypes.g:3781:2: ( ruleFAnnotation )
            {
            // InternalDatatypes.g:3781:2: ( ruleFAnnotation )
            // InternalDatatypes.g:3782:3: ruleFAnnotation
            {
             before(grammarAccess.getFAnnotationBlockAccess().getElementsFAnnotationParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFAnnotation();

            state._fsp--;

             after(grammarAccess.getFAnnotationBlockAccess().getElementsFAnnotationParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FAnnotationBlock__ElementsAssignment_1"


    // $ANTLR start "rule__FAnnotation__RawTextAssignment"
    // InternalDatatypes.g:3791:1: rule__FAnnotation__RawTextAssignment : ( RULE_ANNOTATION_STRING ) ;
    public final void rule__FAnnotation__RawTextAssignment() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3795:1: ( ( RULE_ANNOTATION_STRING ) )
            // InternalDatatypes.g:3796:2: ( RULE_ANNOTATION_STRING )
            {
            // InternalDatatypes.g:3796:2: ( RULE_ANNOTATION_STRING )
            // InternalDatatypes.g:3797:3: RULE_ANNOTATION_STRING
            {
             before(grammarAccess.getFAnnotationAccess().getRawTextANNOTATION_STRINGTerminalRuleCall_0()); 
            match(input,RULE_ANNOTATION_STRING,FOLLOW_2); 
             after(grammarAccess.getFAnnotationAccess().getRawTextANNOTATION_STRINGTerminalRuleCall_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FAnnotation__RawTextAssignment"


    // $ANTLR start "rule__FTypeCollection__CommentAssignment_1"
    // InternalDatatypes.g:3806:1: rule__FTypeCollection__CommentAssignment_1 : ( ruleFAnnotationBlock ) ;
    public final void rule__FTypeCollection__CommentAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3810:1: ( ( ruleFAnnotationBlock ) )
            // InternalDatatypes.g:3811:2: ( ruleFAnnotationBlock )
            {
            // InternalDatatypes.g:3811:2: ( ruleFAnnotationBlock )
            // InternalDatatypes.g:3812:3: ruleFAnnotationBlock
            {
             before(grammarAccess.getFTypeCollectionAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFAnnotationBlock();

            state._fsp--;

             after(grammarAccess.getFTypeCollectionAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__CommentAssignment_1"


    // $ANTLR start "rule__FTypeCollection__NameAssignment_3"
    // InternalDatatypes.g:3821:1: rule__FTypeCollection__NameAssignment_3 : ( RULE_ID ) ;
    public final void rule__FTypeCollection__NameAssignment_3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3825:1: ( ( RULE_ID ) )
            // InternalDatatypes.g:3826:2: ( RULE_ID )
            {
            // InternalDatatypes.g:3826:2: ( RULE_ID )
            // InternalDatatypes.g:3827:3: RULE_ID
            {
             before(grammarAccess.getFTypeCollectionAccess().getNameIDTerminalRuleCall_3_0()); 
            match(input,RULE_ID,FOLLOW_2); 
             after(grammarAccess.getFTypeCollectionAccess().getNameIDTerminalRuleCall_3_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__NameAssignment_3"


    // $ANTLR start "rule__FTypeCollection__VersionAssignment_5_1"
    // InternalDatatypes.g:3836:1: rule__FTypeCollection__VersionAssignment_5_1 : ( ruleFVersion ) ;
    public final void rule__FTypeCollection__VersionAssignment_5_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3840:1: ( ( ruleFVersion ) )
            // InternalDatatypes.g:3841:2: ( ruleFVersion )
            {
            // InternalDatatypes.g:3841:2: ( ruleFVersion )
            // InternalDatatypes.g:3842:3: ruleFVersion
            {
             before(grammarAccess.getFTypeCollectionAccess().getVersionFVersionParserRuleCall_5_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFVersion();

            state._fsp--;

             after(grammarAccess.getFTypeCollectionAccess().getVersionFVersionParserRuleCall_5_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__VersionAssignment_5_1"


    // $ANTLR start "rule__FTypeCollection__TypesAssignment_6"
    // InternalDatatypes.g:3851:1: rule__FTypeCollection__TypesAssignment_6 : ( ruleFType ) ;
    public final void rule__FTypeCollection__TypesAssignment_6() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3855:1: ( ( ruleFType ) )
            // InternalDatatypes.g:3856:2: ( ruleFType )
            {
            // InternalDatatypes.g:3856:2: ( ruleFType )
            // InternalDatatypes.g:3857:3: ruleFType
            {
             before(grammarAccess.getFTypeCollectionAccess().getTypesFTypeParserRuleCall_6_0()); 
            pushFollow(FOLLOW_2);
            ruleFType();

            state._fsp--;

             after(grammarAccess.getFTypeCollectionAccess().getTypesFTypeParserRuleCall_6_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeCollection__TypesAssignment_6"


    // $ANTLR start "rule__FMessageCollection__CommentAssignment_1"
    // InternalDatatypes.g:3866:1: rule__FMessageCollection__CommentAssignment_1 : ( ruleFAnnotationBlock ) ;
    public final void rule__FMessageCollection__CommentAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3870:1: ( ( ruleFAnnotationBlock ) )
            // InternalDatatypes.g:3871:2: ( ruleFAnnotationBlock )
            {
            // InternalDatatypes.g:3871:2: ( ruleFAnnotationBlock )
            // InternalDatatypes.g:3872:3: ruleFAnnotationBlock
            {
             before(grammarAccess.getFMessageCollectionAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFAnnotationBlock();

            state._fsp--;

             after(grammarAccess.getFMessageCollectionAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__CommentAssignment_1"


    // $ANTLR start "rule__FMessageCollection__NameAssignment_3"
    // InternalDatatypes.g:3881:1: rule__FMessageCollection__NameAssignment_3 : ( RULE_ID ) ;
    public final void rule__FMessageCollection__NameAssignment_3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3885:1: ( ( RULE_ID ) )
            // InternalDatatypes.g:3886:2: ( RULE_ID )
            {
            // InternalDatatypes.g:3886:2: ( RULE_ID )
            // InternalDatatypes.g:3887:3: RULE_ID
            {
             before(grammarAccess.getFMessageCollectionAccess().getNameIDTerminalRuleCall_3_0()); 
            match(input,RULE_ID,FOLLOW_2); 
             after(grammarAccess.getFMessageCollectionAccess().getNameIDTerminalRuleCall_3_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__NameAssignment_3"


    // $ANTLR start "rule__FMessageCollection__VersionAssignment_5_1"
    // InternalDatatypes.g:3896:1: rule__FMessageCollection__VersionAssignment_5_1 : ( ruleFVersion ) ;
    public final void rule__FMessageCollection__VersionAssignment_5_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3900:1: ( ( ruleFVersion ) )
            // InternalDatatypes.g:3901:2: ( ruleFVersion )
            {
            // InternalDatatypes.g:3901:2: ( ruleFVersion )
            // InternalDatatypes.g:3902:3: ruleFVersion
            {
             before(grammarAccess.getFMessageCollectionAccess().getVersionFVersionParserRuleCall_5_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFVersion();

            state._fsp--;

             after(grammarAccess.getFMessageCollectionAccess().getVersionFVersionParserRuleCall_5_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__VersionAssignment_5_1"


    // $ANTLR start "rule__FMessageCollection__MessagesAssignment_6"
    // InternalDatatypes.g:3911:1: rule__FMessageCollection__MessagesAssignment_6 : ( ruleFMessage ) ;
    public final void rule__FMessageCollection__MessagesAssignment_6() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3915:1: ( ( ruleFMessage ) )
            // InternalDatatypes.g:3916:2: ( ruleFMessage )
            {
            // InternalDatatypes.g:3916:2: ( ruleFMessage )
            // InternalDatatypes.g:3917:3: ruleFMessage
            {
             before(grammarAccess.getFMessageCollectionAccess().getMessagesFMessageParserRuleCall_6_0()); 
            pushFollow(FOLLOW_2);
            ruleFMessage();

            state._fsp--;

             after(grammarAccess.getFMessageCollectionAccess().getMessagesFMessageParserRuleCall_6_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessageCollection__MessagesAssignment_6"


    // $ANTLR start "rule__FMessage__DerivedAssignment_1"
    // InternalDatatypes.g:3926:1: rule__FMessage__DerivedAssignment_1 : ( ( ruleFQN ) ) ;
    public final void rule__FMessage__DerivedAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3930:1: ( ( ( ruleFQN ) ) )
            // InternalDatatypes.g:3931:2: ( ( ruleFQN ) )
            {
            // InternalDatatypes.g:3931:2: ( ( ruleFQN ) )
            // InternalDatatypes.g:3932:3: ( ruleFQN )
            {
             before(grammarAccess.getFMessageAccess().getDerivedFStructTypeCrossReference_1_0()); 
            // InternalDatatypes.g:3933:3: ( ruleFQN )
            // InternalDatatypes.g:3934:4: ruleFQN
            {
             before(grammarAccess.getFMessageAccess().getDerivedFStructTypeFQNParserRuleCall_1_0_1()); 
            pushFollow(FOLLOW_2);
            ruleFQN();

            state._fsp--;

             after(grammarAccess.getFMessageAccess().getDerivedFStructTypeFQNParserRuleCall_1_0_1()); 

            }

             after(grammarAccess.getFMessageAccess().getDerivedFStructTypeCrossReference_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__DerivedAssignment_1"


    // $ANTLR start "rule__FMessage__NameAssignment_2"
    // InternalDatatypes.g:3945:1: rule__FMessage__NameAssignment_2 : ( RULE_ID ) ;
    public final void rule__FMessage__NameAssignment_2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3949:1: ( ( RULE_ID ) )
            // InternalDatatypes.g:3950:2: ( RULE_ID )
            {
            // InternalDatatypes.g:3950:2: ( RULE_ID )
            // InternalDatatypes.g:3951:3: RULE_ID
            {
             before(grammarAccess.getFMessageAccess().getNameIDTerminalRuleCall_2_0()); 
            match(input,RULE_ID,FOLLOW_2); 
             after(grammarAccess.getFMessageAccess().getNameIDTerminalRuleCall_2_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__NameAssignment_2"


    // $ANTLR start "rule__FMessage__KeyAssignment_3_1"
    // InternalDatatypes.g:3960:1: rule__FMessage__KeyAssignment_3_1 : ( ( ruleFQN ) ) ;
    public final void rule__FMessage__KeyAssignment_3_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3964:1: ( ( ( ruleFQN ) ) )
            // InternalDatatypes.g:3965:2: ( ( ruleFQN ) )
            {
            // InternalDatatypes.g:3965:2: ( ( ruleFQN ) )
            // InternalDatatypes.g:3966:3: ( ruleFQN )
            {
             before(grammarAccess.getFMessageAccess().getKeyFFieldCrossReference_3_1_0()); 
            // InternalDatatypes.g:3967:3: ( ruleFQN )
            // InternalDatatypes.g:3968:4: ruleFQN
            {
             before(grammarAccess.getFMessageAccess().getKeyFFieldFQNParserRuleCall_3_1_0_1()); 
            pushFollow(FOLLOW_2);
            ruleFQN();

            state._fsp--;

             after(grammarAccess.getFMessageAccess().getKeyFFieldFQNParserRuleCall_3_1_0_1()); 

            }

             after(grammarAccess.getFMessageAccess().getKeyFFieldCrossReference_3_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMessage__KeyAssignment_3_1"


    // $ANTLR start "rule__FVersion__MajorAssignment_3"
    // InternalDatatypes.g:3979:1: rule__FVersion__MajorAssignment_3 : ( RULE_INT ) ;
    public final void rule__FVersion__MajorAssignment_3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3983:1: ( ( RULE_INT ) )
            // InternalDatatypes.g:3984:2: ( RULE_INT )
            {
            // InternalDatatypes.g:3984:2: ( RULE_INT )
            // InternalDatatypes.g:3985:3: RULE_INT
            {
             before(grammarAccess.getFVersionAccess().getMajorINTTerminalRuleCall_3_0()); 
            match(input,RULE_INT,FOLLOW_2); 
             after(grammarAccess.getFVersionAccess().getMajorINTTerminalRuleCall_3_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__MajorAssignment_3"


    // $ANTLR start "rule__FVersion__MinorAssignment_5"
    // InternalDatatypes.g:3994:1: rule__FVersion__MinorAssignment_5 : ( RULE_INT ) ;
    public final void rule__FVersion__MinorAssignment_5() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:3998:1: ( ( RULE_INT ) )
            // InternalDatatypes.g:3999:2: ( RULE_INT )
            {
            // InternalDatatypes.g:3999:2: ( RULE_INT )
            // InternalDatatypes.g:4000:3: RULE_INT
            {
             before(grammarAccess.getFVersionAccess().getMinorINTTerminalRuleCall_5_0()); 
            match(input,RULE_INT,FOLLOW_2); 
             after(grammarAccess.getFVersionAccess().getMinorINTTerminalRuleCall_5_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FVersion__MinorAssignment_5"


    // $ANTLR start "rule__FTypeRef__PredefinedAssignment_0"
    // InternalDatatypes.g:4009:1: rule__FTypeRef__PredefinedAssignment_0 : ( ruleFBasicTypeId ) ;
    public final void rule__FTypeRef__PredefinedAssignment_0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4013:1: ( ( ruleFBasicTypeId ) )
            // InternalDatatypes.g:4014:2: ( ruleFBasicTypeId )
            {
            // InternalDatatypes.g:4014:2: ( ruleFBasicTypeId )
            // InternalDatatypes.g:4015:3: ruleFBasicTypeId
            {
             before(grammarAccess.getFTypeRefAccess().getPredefinedFBasicTypeIdEnumRuleCall_0_0()); 
            pushFollow(FOLLOW_2);
            ruleFBasicTypeId();

            state._fsp--;

             after(grammarAccess.getFTypeRefAccess().getPredefinedFBasicTypeIdEnumRuleCall_0_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeRef__PredefinedAssignment_0"


    // $ANTLR start "rule__FTypeRef__DerivedAssignment_1"
    // InternalDatatypes.g:4024:1: rule__FTypeRef__DerivedAssignment_1 : ( ( ruleFQN ) ) ;
    public final void rule__FTypeRef__DerivedAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4028:1: ( ( ( ruleFQN ) ) )
            // InternalDatatypes.g:4029:2: ( ( ruleFQN ) )
            {
            // InternalDatatypes.g:4029:2: ( ( ruleFQN ) )
            // InternalDatatypes.g:4030:3: ( ruleFQN )
            {
             before(grammarAccess.getFTypeRefAccess().getDerivedFTypeCrossReference_1_0()); 
            // InternalDatatypes.g:4031:3: ( ruleFQN )
            // InternalDatatypes.g:4032:4: ruleFQN
            {
             before(grammarAccess.getFTypeRefAccess().getDerivedFTypeFQNParserRuleCall_1_0_1()); 
            pushFollow(FOLLOW_2);
            ruleFQN();

            state._fsp--;

             after(grammarAccess.getFTypeRefAccess().getDerivedFTypeFQNParserRuleCall_1_0_1()); 

            }

             after(grammarAccess.getFTypeRefAccess().getDerivedFTypeCrossReference_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeRef__DerivedAssignment_1"


    // $ANTLR start "rule__FArrayType__CommentAssignment_1"
    // InternalDatatypes.g:4043:1: rule__FArrayType__CommentAssignment_1 : ( ruleFAnnotationBlock ) ;
    public final void rule__FArrayType__CommentAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4047:1: ( ( ruleFAnnotationBlock ) )
            // InternalDatatypes.g:4048:2: ( ruleFAnnotationBlock )
            {
            // InternalDatatypes.g:4048:2: ( ruleFAnnotationBlock )
            // InternalDatatypes.g:4049:3: ruleFAnnotationBlock
            {
             before(grammarAccess.getFArrayTypeAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFAnnotationBlock();

            state._fsp--;

             after(grammarAccess.getFArrayTypeAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__CommentAssignment_1"


    // $ANTLR start "rule__FArrayType__NameAssignment_3"
    // InternalDatatypes.g:4058:1: rule__FArrayType__NameAssignment_3 : ( RULE_ID ) ;
    public final void rule__FArrayType__NameAssignment_3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4062:1: ( ( RULE_ID ) )
            // InternalDatatypes.g:4063:2: ( RULE_ID )
            {
            // InternalDatatypes.g:4063:2: ( RULE_ID )
            // InternalDatatypes.g:4064:3: RULE_ID
            {
             before(grammarAccess.getFArrayTypeAccess().getNameIDTerminalRuleCall_3_0()); 
            match(input,RULE_ID,FOLLOW_2); 
             after(grammarAccess.getFArrayTypeAccess().getNameIDTerminalRuleCall_3_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__NameAssignment_3"


    // $ANTLR start "rule__FArrayType__ElementTypeAssignment_5"
    // InternalDatatypes.g:4073:1: rule__FArrayType__ElementTypeAssignment_5 : ( ruleFTypeRef ) ;
    public final void rule__FArrayType__ElementTypeAssignment_5() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4077:1: ( ( ruleFTypeRef ) )
            // InternalDatatypes.g:4078:2: ( ruleFTypeRef )
            {
            // InternalDatatypes.g:4078:2: ( ruleFTypeRef )
            // InternalDatatypes.g:4079:3: ruleFTypeRef
            {
             before(grammarAccess.getFArrayTypeAccess().getElementTypeFTypeRefParserRuleCall_5_0()); 
            pushFollow(FOLLOW_2);
            ruleFTypeRef();

            state._fsp--;

             after(grammarAccess.getFArrayTypeAccess().getElementTypeFTypeRefParserRuleCall_5_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FArrayType__ElementTypeAssignment_5"


    // $ANTLR start "rule__FTypeDef__CommentAssignment_1"
    // InternalDatatypes.g:4088:1: rule__FTypeDef__CommentAssignment_1 : ( ruleFAnnotationBlock ) ;
    public final void rule__FTypeDef__CommentAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4092:1: ( ( ruleFAnnotationBlock ) )
            // InternalDatatypes.g:4093:2: ( ruleFAnnotationBlock )
            {
            // InternalDatatypes.g:4093:2: ( ruleFAnnotationBlock )
            // InternalDatatypes.g:4094:3: ruleFAnnotationBlock
            {
             before(grammarAccess.getFTypeDefAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFAnnotationBlock();

            state._fsp--;

             after(grammarAccess.getFTypeDefAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__CommentAssignment_1"


    // $ANTLR start "rule__FTypeDef__NameAssignment_3"
    // InternalDatatypes.g:4103:1: rule__FTypeDef__NameAssignment_3 : ( RULE_ID ) ;
    public final void rule__FTypeDef__NameAssignment_3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4107:1: ( ( RULE_ID ) )
            // InternalDatatypes.g:4108:2: ( RULE_ID )
            {
            // InternalDatatypes.g:4108:2: ( RULE_ID )
            // InternalDatatypes.g:4109:3: RULE_ID
            {
             before(grammarAccess.getFTypeDefAccess().getNameIDTerminalRuleCall_3_0()); 
            match(input,RULE_ID,FOLLOW_2); 
             after(grammarAccess.getFTypeDefAccess().getNameIDTerminalRuleCall_3_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__NameAssignment_3"


    // $ANTLR start "rule__FTypeDef__ActualTypeAssignment_5"
    // InternalDatatypes.g:4118:1: rule__FTypeDef__ActualTypeAssignment_5 : ( ruleFTypeRef ) ;
    public final void rule__FTypeDef__ActualTypeAssignment_5() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4122:1: ( ( ruleFTypeRef ) )
            // InternalDatatypes.g:4123:2: ( ruleFTypeRef )
            {
            // InternalDatatypes.g:4123:2: ( ruleFTypeRef )
            // InternalDatatypes.g:4124:3: ruleFTypeRef
            {
             before(grammarAccess.getFTypeDefAccess().getActualTypeFTypeRefParserRuleCall_5_0()); 
            pushFollow(FOLLOW_2);
            ruleFTypeRef();

            state._fsp--;

             after(grammarAccess.getFTypeDefAccess().getActualTypeFTypeRefParserRuleCall_5_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FTypeDef__ActualTypeAssignment_5"


    // $ANTLR start "rule__FStructType__CommentAssignment_1"
    // InternalDatatypes.g:4133:1: rule__FStructType__CommentAssignment_1 : ( ruleFAnnotationBlock ) ;
    public final void rule__FStructType__CommentAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4137:1: ( ( ruleFAnnotationBlock ) )
            // InternalDatatypes.g:4138:2: ( ruleFAnnotationBlock )
            {
            // InternalDatatypes.g:4138:2: ( ruleFAnnotationBlock )
            // InternalDatatypes.g:4139:3: ruleFAnnotationBlock
            {
             before(grammarAccess.getFStructTypeAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFAnnotationBlock();

            state._fsp--;

             after(grammarAccess.getFStructTypeAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__CommentAssignment_1"


    // $ANTLR start "rule__FStructType__NameAssignment_3"
    // InternalDatatypes.g:4148:1: rule__FStructType__NameAssignment_3 : ( RULE_ID ) ;
    public final void rule__FStructType__NameAssignment_3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4152:1: ( ( RULE_ID ) )
            // InternalDatatypes.g:4153:2: ( RULE_ID )
            {
            // InternalDatatypes.g:4153:2: ( RULE_ID )
            // InternalDatatypes.g:4154:3: RULE_ID
            {
             before(grammarAccess.getFStructTypeAccess().getNameIDTerminalRuleCall_3_0()); 
            match(input,RULE_ID,FOLLOW_2); 
             after(grammarAccess.getFStructTypeAccess().getNameIDTerminalRuleCall_3_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__NameAssignment_3"


    // $ANTLR start "rule__FStructType__BaseAssignment_4_1"
    // InternalDatatypes.g:4163:1: rule__FStructType__BaseAssignment_4_1 : ( ( ruleFQN ) ) ;
    public final void rule__FStructType__BaseAssignment_4_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4167:1: ( ( ( ruleFQN ) ) )
            // InternalDatatypes.g:4168:2: ( ( ruleFQN ) )
            {
            // InternalDatatypes.g:4168:2: ( ( ruleFQN ) )
            // InternalDatatypes.g:4169:3: ( ruleFQN )
            {
             before(grammarAccess.getFStructTypeAccess().getBaseFStructTypeCrossReference_4_1_0()); 
            // InternalDatatypes.g:4170:3: ( ruleFQN )
            // InternalDatatypes.g:4171:4: ruleFQN
            {
             before(grammarAccess.getFStructTypeAccess().getBaseFStructTypeFQNParserRuleCall_4_1_0_1()); 
            pushFollow(FOLLOW_2);
            ruleFQN();

            state._fsp--;

             after(grammarAccess.getFStructTypeAccess().getBaseFStructTypeFQNParserRuleCall_4_1_0_1()); 

            }

             after(grammarAccess.getFStructTypeAccess().getBaseFStructTypeCrossReference_4_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__BaseAssignment_4_1"


    // $ANTLR start "rule__FStructType__ElementsAssignment_6"
    // InternalDatatypes.g:4182:1: rule__FStructType__ElementsAssignment_6 : ( ruleFField ) ;
    public final void rule__FStructType__ElementsAssignment_6() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4186:1: ( ( ruleFField ) )
            // InternalDatatypes.g:4187:2: ( ruleFField )
            {
            // InternalDatatypes.g:4187:2: ( ruleFField )
            // InternalDatatypes.g:4188:3: ruleFField
            {
             before(grammarAccess.getFStructTypeAccess().getElementsFFieldParserRuleCall_6_0()); 
            pushFollow(FOLLOW_2);
            ruleFField();

            state._fsp--;

             after(grammarAccess.getFStructTypeAccess().getElementsFFieldParserRuleCall_6_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FStructType__ElementsAssignment_6"


    // $ANTLR start "rule__FEnumerationType__CommentAssignment_1"
    // InternalDatatypes.g:4197:1: rule__FEnumerationType__CommentAssignment_1 : ( ruleFAnnotationBlock ) ;
    public final void rule__FEnumerationType__CommentAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4201:1: ( ( ruleFAnnotationBlock ) )
            // InternalDatatypes.g:4202:2: ( ruleFAnnotationBlock )
            {
            // InternalDatatypes.g:4202:2: ( ruleFAnnotationBlock )
            // InternalDatatypes.g:4203:3: ruleFAnnotationBlock
            {
             before(grammarAccess.getFEnumerationTypeAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFAnnotationBlock();

            state._fsp--;

             after(grammarAccess.getFEnumerationTypeAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__CommentAssignment_1"


    // $ANTLR start "rule__FEnumerationType__NameAssignment_3"
    // InternalDatatypes.g:4212:1: rule__FEnumerationType__NameAssignment_3 : ( RULE_ID ) ;
    public final void rule__FEnumerationType__NameAssignment_3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4216:1: ( ( RULE_ID ) )
            // InternalDatatypes.g:4217:2: ( RULE_ID )
            {
            // InternalDatatypes.g:4217:2: ( RULE_ID )
            // InternalDatatypes.g:4218:3: RULE_ID
            {
             before(grammarAccess.getFEnumerationTypeAccess().getNameIDTerminalRuleCall_3_0()); 
            match(input,RULE_ID,FOLLOW_2); 
             after(grammarAccess.getFEnumerationTypeAccess().getNameIDTerminalRuleCall_3_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__NameAssignment_3"


    // $ANTLR start "rule__FEnumerationType__BaseAssignment_4_1"
    // InternalDatatypes.g:4227:1: rule__FEnumerationType__BaseAssignment_4_1 : ( ( ruleFQN ) ) ;
    public final void rule__FEnumerationType__BaseAssignment_4_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4231:1: ( ( ( ruleFQN ) ) )
            // InternalDatatypes.g:4232:2: ( ( ruleFQN ) )
            {
            // InternalDatatypes.g:4232:2: ( ( ruleFQN ) )
            // InternalDatatypes.g:4233:3: ( ruleFQN )
            {
             before(grammarAccess.getFEnumerationTypeAccess().getBaseFEnumerationTypeCrossReference_4_1_0()); 
            // InternalDatatypes.g:4234:3: ( ruleFQN )
            // InternalDatatypes.g:4235:4: ruleFQN
            {
             before(grammarAccess.getFEnumerationTypeAccess().getBaseFEnumerationTypeFQNParserRuleCall_4_1_0_1()); 
            pushFollow(FOLLOW_2);
            ruleFQN();

            state._fsp--;

             after(grammarAccess.getFEnumerationTypeAccess().getBaseFEnumerationTypeFQNParserRuleCall_4_1_0_1()); 

            }

             after(grammarAccess.getFEnumerationTypeAccess().getBaseFEnumerationTypeCrossReference_4_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__BaseAssignment_4_1"


    // $ANTLR start "rule__FEnumerationType__EnumeratorsAssignment_6_0"
    // InternalDatatypes.g:4246:1: rule__FEnumerationType__EnumeratorsAssignment_6_0 : ( ruleFEnumerator ) ;
    public final void rule__FEnumerationType__EnumeratorsAssignment_6_0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4250:1: ( ( ruleFEnumerator ) )
            // InternalDatatypes.g:4251:2: ( ruleFEnumerator )
            {
            // InternalDatatypes.g:4251:2: ( ruleFEnumerator )
            // InternalDatatypes.g:4252:3: ruleFEnumerator
            {
             before(grammarAccess.getFEnumerationTypeAccess().getEnumeratorsFEnumeratorParserRuleCall_6_0_0()); 
            pushFollow(FOLLOW_2);
            ruleFEnumerator();

            state._fsp--;

             after(grammarAccess.getFEnumerationTypeAccess().getEnumeratorsFEnumeratorParserRuleCall_6_0_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__EnumeratorsAssignment_6_0"


    // $ANTLR start "rule__FEnumerationType__EnumeratorsAssignment_6_1_1"
    // InternalDatatypes.g:4261:1: rule__FEnumerationType__EnumeratorsAssignment_6_1_1 : ( ruleFEnumerator ) ;
    public final void rule__FEnumerationType__EnumeratorsAssignment_6_1_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4265:1: ( ( ruleFEnumerator ) )
            // InternalDatatypes.g:4266:2: ( ruleFEnumerator )
            {
            // InternalDatatypes.g:4266:2: ( ruleFEnumerator )
            // InternalDatatypes.g:4267:3: ruleFEnumerator
            {
             before(grammarAccess.getFEnumerationTypeAccess().getEnumeratorsFEnumeratorParserRuleCall_6_1_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFEnumerator();

            state._fsp--;

             after(grammarAccess.getFEnumerationTypeAccess().getEnumeratorsFEnumeratorParserRuleCall_6_1_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerationType__EnumeratorsAssignment_6_1_1"


    // $ANTLR start "rule__FEnumerator__CommentAssignment_1"
    // InternalDatatypes.g:4276:1: rule__FEnumerator__CommentAssignment_1 : ( ruleFAnnotationBlock ) ;
    public final void rule__FEnumerator__CommentAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4280:1: ( ( ruleFAnnotationBlock ) )
            // InternalDatatypes.g:4281:2: ( ruleFAnnotationBlock )
            {
            // InternalDatatypes.g:4281:2: ( ruleFAnnotationBlock )
            // InternalDatatypes.g:4282:3: ruleFAnnotationBlock
            {
             before(grammarAccess.getFEnumeratorAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFAnnotationBlock();

            state._fsp--;

             after(grammarAccess.getFEnumeratorAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__CommentAssignment_1"


    // $ANTLR start "rule__FEnumerator__NameAssignment_2"
    // InternalDatatypes.g:4291:1: rule__FEnumerator__NameAssignment_2 : ( RULE_ID ) ;
    public final void rule__FEnumerator__NameAssignment_2() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4295:1: ( ( RULE_ID ) )
            // InternalDatatypes.g:4296:2: ( RULE_ID )
            {
            // InternalDatatypes.g:4296:2: ( RULE_ID )
            // InternalDatatypes.g:4297:3: RULE_ID
            {
             before(grammarAccess.getFEnumeratorAccess().getNameIDTerminalRuleCall_2_0()); 
            match(input,RULE_ID,FOLLOW_2); 
             after(grammarAccess.getFEnumeratorAccess().getNameIDTerminalRuleCall_2_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__NameAssignment_2"


    // $ANTLR start "rule__FEnumerator__ValueAssignment_3_1"
    // InternalDatatypes.g:4306:1: rule__FEnumerator__ValueAssignment_3_1 : ( RULE_STRING ) ;
    public final void rule__FEnumerator__ValueAssignment_3_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4310:1: ( ( RULE_STRING ) )
            // InternalDatatypes.g:4311:2: ( RULE_STRING )
            {
            // InternalDatatypes.g:4311:2: ( RULE_STRING )
            // InternalDatatypes.g:4312:3: RULE_STRING
            {
             before(grammarAccess.getFEnumeratorAccess().getValueSTRINGTerminalRuleCall_3_1_0()); 
            match(input,RULE_STRING,FOLLOW_2); 
             after(grammarAccess.getFEnumeratorAccess().getValueSTRINGTerminalRuleCall_3_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FEnumerator__ValueAssignment_3_1"


    // $ANTLR start "rule__FMapType__CommentAssignment_1"
    // InternalDatatypes.g:4321:1: rule__FMapType__CommentAssignment_1 : ( ruleFAnnotationBlock ) ;
    public final void rule__FMapType__CommentAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4325:1: ( ( ruleFAnnotationBlock ) )
            // InternalDatatypes.g:4326:2: ( ruleFAnnotationBlock )
            {
            // InternalDatatypes.g:4326:2: ( ruleFAnnotationBlock )
            // InternalDatatypes.g:4327:3: ruleFAnnotationBlock
            {
             before(grammarAccess.getFMapTypeAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFAnnotationBlock();

            state._fsp--;

             after(grammarAccess.getFMapTypeAccess().getCommentFAnnotationBlockParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__CommentAssignment_1"


    // $ANTLR start "rule__FMapType__NameAssignment_3"
    // InternalDatatypes.g:4336:1: rule__FMapType__NameAssignment_3 : ( RULE_ID ) ;
    public final void rule__FMapType__NameAssignment_3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4340:1: ( ( RULE_ID ) )
            // InternalDatatypes.g:4341:2: ( RULE_ID )
            {
            // InternalDatatypes.g:4341:2: ( RULE_ID )
            // InternalDatatypes.g:4342:3: RULE_ID
            {
             before(grammarAccess.getFMapTypeAccess().getNameIDTerminalRuleCall_3_0()); 
            match(input,RULE_ID,FOLLOW_2); 
             after(grammarAccess.getFMapTypeAccess().getNameIDTerminalRuleCall_3_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__NameAssignment_3"


    // $ANTLR start "rule__FMapType__KeyTypeAssignment_5"
    // InternalDatatypes.g:4351:1: rule__FMapType__KeyTypeAssignment_5 : ( ruleFTypeRef ) ;
    public final void rule__FMapType__KeyTypeAssignment_5() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4355:1: ( ( ruleFTypeRef ) )
            // InternalDatatypes.g:4356:2: ( ruleFTypeRef )
            {
            // InternalDatatypes.g:4356:2: ( ruleFTypeRef )
            // InternalDatatypes.g:4357:3: ruleFTypeRef
            {
             before(grammarAccess.getFMapTypeAccess().getKeyTypeFTypeRefParserRuleCall_5_0()); 
            pushFollow(FOLLOW_2);
            ruleFTypeRef();

            state._fsp--;

             after(grammarAccess.getFMapTypeAccess().getKeyTypeFTypeRefParserRuleCall_5_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__KeyTypeAssignment_5"


    // $ANTLR start "rule__FMapType__ValueTypeAssignment_7"
    // InternalDatatypes.g:4366:1: rule__FMapType__ValueTypeAssignment_7 : ( ruleFTypeRef ) ;
    public final void rule__FMapType__ValueTypeAssignment_7() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4370:1: ( ( ruleFTypeRef ) )
            // InternalDatatypes.g:4371:2: ( ruleFTypeRef )
            {
            // InternalDatatypes.g:4371:2: ( ruleFTypeRef )
            // InternalDatatypes.g:4372:3: ruleFTypeRef
            {
             before(grammarAccess.getFMapTypeAccess().getValueTypeFTypeRefParserRuleCall_7_0()); 
            pushFollow(FOLLOW_2);
            ruleFTypeRef();

            state._fsp--;

             after(grammarAccess.getFMapTypeAccess().getValueTypeFTypeRefParserRuleCall_7_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FMapType__ValueTypeAssignment_7"


    // $ANTLR start "rule__FField__CommentAssignment_0"
    // InternalDatatypes.g:4381:1: rule__FField__CommentAssignment_0 : ( ruleFAnnotationBlock ) ;
    public final void rule__FField__CommentAssignment_0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4385:1: ( ( ruleFAnnotationBlock ) )
            // InternalDatatypes.g:4386:2: ( ruleFAnnotationBlock )
            {
            // InternalDatatypes.g:4386:2: ( ruleFAnnotationBlock )
            // InternalDatatypes.g:4387:3: ruleFAnnotationBlock
            {
             before(grammarAccess.getFFieldAccess().getCommentFAnnotationBlockParserRuleCall_0_0()); 
            pushFollow(FOLLOW_2);
            ruleFAnnotationBlock();

            state._fsp--;

             after(grammarAccess.getFFieldAccess().getCommentFAnnotationBlockParserRuleCall_0_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__CommentAssignment_0"


    // $ANTLR start "rule__FField__TypeAssignment_1"
    // InternalDatatypes.g:4396:1: rule__FField__TypeAssignment_1 : ( ruleFTypeRef ) ;
    public final void rule__FField__TypeAssignment_1() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4400:1: ( ( ruleFTypeRef ) )
            // InternalDatatypes.g:4401:2: ( ruleFTypeRef )
            {
            // InternalDatatypes.g:4401:2: ( ruleFTypeRef )
            // InternalDatatypes.g:4402:3: ruleFTypeRef
            {
             before(grammarAccess.getFFieldAccess().getTypeFTypeRefParserRuleCall_1_0()); 
            pushFollow(FOLLOW_2);
            ruleFTypeRef();

            state._fsp--;

             after(grammarAccess.getFFieldAccess().getTypeFTypeRefParserRuleCall_1_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__TypeAssignment_1"


    // $ANTLR start "rule__FField__ArrayAssignment_2_0"
    // InternalDatatypes.g:4411:1: rule__FField__ArrayAssignment_2_0 : ( ( '[' ) ) ;
    public final void rule__FField__ArrayAssignment_2_0() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4415:1: ( ( ( '[' ) ) )
            // InternalDatatypes.g:4416:2: ( ( '[' ) )
            {
            // InternalDatatypes.g:4416:2: ( ( '[' ) )
            // InternalDatatypes.g:4417:3: ( '[' )
            {
             before(grammarAccess.getFFieldAccess().getArrayLeftSquareBracketKeyword_2_0_0()); 
            // InternalDatatypes.g:4418:3: ( '[' )
            // InternalDatatypes.g:4419:4: '['
            {
             before(grammarAccess.getFFieldAccess().getArrayLeftSquareBracketKeyword_2_0_0()); 
            match(input,51,FOLLOW_2); 
             after(grammarAccess.getFFieldAccess().getArrayLeftSquareBracketKeyword_2_0_0()); 

            }

             after(grammarAccess.getFFieldAccess().getArrayLeftSquareBracketKeyword_2_0_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__ArrayAssignment_2_0"


    // $ANTLR start "rule__FField__NameAssignment_3"
    // InternalDatatypes.g:4430:1: rule__FField__NameAssignment_3 : ( RULE_ID ) ;
    public final void rule__FField__NameAssignment_3() throws RecognitionException {

        		int stackSize = keepStackSize();
        	
        try {
            // InternalDatatypes.g:4434:1: ( ( RULE_ID ) )
            // InternalDatatypes.g:4435:2: ( RULE_ID )
            {
            // InternalDatatypes.g:4435:2: ( RULE_ID )
            // InternalDatatypes.g:4436:3: RULE_ID
            {
             before(grammarAccess.getFFieldAccess().getNameIDTerminalRuleCall_3_0()); 
            match(input,RULE_ID,FOLLOW_2); 
             after(grammarAccess.getFFieldAccess().getNameIDTerminalRuleCall_3_0()); 

            }


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {

            	restoreStackSize(stackSize);

        }
        return ;
    }
    // $ANTLR end "rule__FField__NameAssignment_3"

    // Delegated rules


    protected DFA1 dfa1 = new DFA1(this);
    protected DFA3 dfa3 = new DFA3(this);
    static final String dfa_1s = "\7\uffff";
    static final String dfa_2s = "\1\35\1\5\2\uffff\2\5\1\37";
    static final String dfa_3s = "\1\43\1\5\2\uffff\2\36\1\43";
    static final String dfa_4s = "\2\uffff\1\1\1\2\3\uffff";
    static final String dfa_5s = "\7\uffff}>";
    static final String[] dfa_6s = {
            "\1\1\1\uffff\1\2\3\uffff\1\3",
            "\1\4",
            "",
            "",
            "\1\5\30\uffff\1\6",
            "\1\5\30\uffff\1\6",
            "\1\2\3\uffff\1\3"
    };

    static final short[] dfa_1 = DFA.unpackEncodedString(dfa_1s);
    static final char[] dfa_2 = DFA.unpackEncodedStringToUnsignedChars(dfa_2s);
    static final char[] dfa_3 = DFA.unpackEncodedStringToUnsignedChars(dfa_3s);
    static final short[] dfa_4 = DFA.unpackEncodedString(dfa_4s);
    static final short[] dfa_5 = DFA.unpackEncodedString(dfa_5s);
    static final short[][] dfa_6 = unpackEncodedStringArray(dfa_6s);

    class DFA1 extends DFA {

        public DFA1(BaseRecognizer recognizer) {
            this.recognizer = recognizer;
            this.decisionNumber = 1;
            this.eot = dfa_1;
            this.eof = dfa_1;
            this.min = dfa_2;
            this.max = dfa_3;
            this.accept = dfa_4;
            this.special = dfa_5;
            this.transition = dfa_6;
        }
        public String getDescription() {
            return "568:1: rule__Model__Alternatives_3 : ( ( ( rule__Model__TypeCollectionsAssignment_3_0 ) ) | ( ( rule__Model__MessageCollectionsAssignment_3_1 ) ) );";
        }
    }
    static final String dfa_7s = "\12\uffff";
    static final String dfa_8s = "\1\35\1\5\5\uffff\2\5\1\47";
    static final String dfa_9s = "\1\60\1\5\5\uffff\2\36\1\60";
    static final String dfa_10s = "\2\uffff\1\1\1\2\1\3\1\4\1\5\3\uffff";
    static final String dfa_11s = "\12\uffff}>";
    static final String[] dfa_12s = {
            "\1\1\11\uffff\1\2\1\uffff\1\6\1\uffff\1\4\1\uffff\1\3\2\uffff\1\5",
            "\1\7",
            "",
            "",
            "",
            "",
            "",
            "\1\10\30\uffff\1\11",
            "\1\10\30\uffff\1\11",
            "\1\2\1\uffff\1\6\1\uffff\1\4\1\uffff\1\3\2\uffff\1\5"
    };

    static final short[] dfa_7 = DFA.unpackEncodedString(dfa_7s);
    static final char[] dfa_8 = DFA.unpackEncodedStringToUnsignedChars(dfa_8s);
    static final char[] dfa_9 = DFA.unpackEncodedStringToUnsignedChars(dfa_9s);
    static final short[] dfa_10 = DFA.unpackEncodedString(dfa_10s);
    static final short[] dfa_11 = DFA.unpackEncodedString(dfa_11s);
    static final short[][] dfa_12 = unpackEncodedStringArray(dfa_12s);

    class DFA3 extends DFA {

        public DFA3(BaseRecognizer recognizer) {
            this.recognizer = recognizer;
            this.decisionNumber = 3;
            this.eot = dfa_7;
            this.eof = dfa_7;
            this.min = dfa_8;
            this.max = dfa_9;
            this.accept = dfa_10;
            this.special = dfa_11;
            this.transition = dfa_12;
        }
        public String getDescription() {
            return "610:1: rule__FType__Alternatives : ( ( ruleFArrayType ) | ( ruleFEnumerationType ) | ( ruleFStructType ) | ( ruleFMapType ) | ( ruleFTypeDef ) );";
        }
    }
 

    public static final BitSet FOLLOW_1 = new BitSet(new long[]{0x0000000000000000L});
    public static final BitSet FOLLOW_2 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_3 = new BitSet(new long[]{0x0000000002000000L});
    public static final BitSet FOLLOW_4 = new BitSet(new long[]{0x00000008A4000000L});
    public static final BitSet FOLLOW_5 = new BitSet(new long[]{0x0000000004000002L});
    public static final BitSet FOLLOW_6 = new BitSet(new long[]{0x00000008A0000002L});
    public static final BitSet FOLLOW_7 = new BitSet(new long[]{0x0000000000000010L});
    public static final BitSet FOLLOW_8 = new BitSet(new long[]{0x0000000008000000L});
    public static final BitSet FOLLOW_9 = new BitSet(new long[]{0x0000000010000000L});
    public static final BitSet FOLLOW_10 = new BitSet(new long[]{0x0000000008000002L});
    public static final BitSet FOLLOW_11 = new BitSet(new long[]{0x0000000000000020L});
    public static final BitSet FOLLOW_12 = new BitSet(new long[]{0x0000000040000000L});
    public static final BitSet FOLLOW_13 = new BitSet(new long[]{0x0000000000000022L});
    public static final BitSet FOLLOW_14 = new BitSet(new long[]{0x00000000A0000000L});
    public static final BitSet FOLLOW_15 = new BitSet(new long[]{0x0000000100000010L});
    public static final BitSet FOLLOW_16 = new BitSet(new long[]{0x00012A8620000000L});
    public static final BitSet FOLLOW_17 = new BitSet(new long[]{0x00012A8020000002L});
    public static final BitSet FOLLOW_18 = new BitSet(new long[]{0x0000000100000000L});
    public static final BitSet FOLLOW_19 = new BitSet(new long[]{0x00000008A0000000L});
    public static final BitSet FOLLOW_20 = new BitSet(new long[]{0x0000000600000010L});
    public static final BitSet FOLLOW_21 = new BitSet(new long[]{0x0000000000000012L});
    public static final BitSet FOLLOW_22 = new BitSet(new long[]{0x0000001000000000L});
    public static final BitSet FOLLOW_23 = new BitSet(new long[]{0x0000002000000000L});
    public static final BitSet FOLLOW_24 = new BitSet(new long[]{0x0000000000000040L});
    public static final BitSet FOLLOW_25 = new BitSet(new long[]{0x0000004000000000L});
    public static final BitSet FOLLOW_26 = new BitSet(new long[]{0x0000000200000000L});
    public static final BitSet FOLLOW_27 = new BitSet(new long[]{0x0000008020000000L});
    public static final BitSet FOLLOW_28 = new BitSet(new long[]{0x0000010000000000L});
    public static final BitSet FOLLOW_29 = new BitSet(new long[]{0x0000000001FFF010L});
    public static final BitSet FOLLOW_30 = new BitSet(new long[]{0x00012A8020000000L});
    public static final BitSet FOLLOW_31 = new BitSet(new long[]{0x0000040000000000L});
    public static final BitSet FOLLOW_32 = new BitSet(new long[]{0x0000080020000000L});
    public static final BitSet FOLLOW_33 = new BitSet(new long[]{0x0000100100000000L});
    public static final BitSet FOLLOW_34 = new BitSet(new long[]{0x0000000221FFF010L});
    public static final BitSet FOLLOW_35 = new BitSet(new long[]{0x0000000021FFF012L});
    public static final BitSet FOLLOW_36 = new BitSet(new long[]{0x0000200020000000L});
    public static final BitSet FOLLOW_37 = new BitSet(new long[]{0x0000000220000010L});
    public static final BitSet FOLLOW_38 = new BitSet(new long[]{0x0000400020000010L});
    public static final BitSet FOLLOW_39 = new BitSet(new long[]{0x0000400020000012L});
    public static final BitSet FOLLOW_40 = new BitSet(new long[]{0x0000000020000010L});
    public static final BitSet FOLLOW_41 = new BitSet(new long[]{0x0000800000000000L});
    public static final BitSet FOLLOW_42 = new BitSet(new long[]{0x0000000000000080L});
    public static final BitSet FOLLOW_43 = new BitSet(new long[]{0x0001000020000000L});
    public static final BitSet FOLLOW_44 = new BitSet(new long[]{0x0002000000000000L});
    public static final BitSet FOLLOW_45 = new BitSet(new long[]{0x0000000021FFF010L});
    public static final BitSet FOLLOW_46 = new BitSet(new long[]{0x0008000000000010L});
    public static final BitSet FOLLOW_47 = new BitSet(new long[]{0x0004000000000000L});

}