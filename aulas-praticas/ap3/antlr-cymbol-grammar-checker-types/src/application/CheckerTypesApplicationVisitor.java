package application;

import java.io.IOException;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

import autogenerated.*;
import walker.CymbolCheckerVisitor;



public class CheckerTypesApplicationVisitor {
	public static ANTLRInputStream getStandardInputStream( ) throws IOException {
		return (new ANTLRInputStream(System.in));
	}
	
	public static ANTLRInputStream getFileInputStream(String filePath) throws IOException {
		return (new ANTLRFileStream(filePath));
	}
	
	public static void main(String[] args) throws IOException {
		ANTLRInputStream input = getStandardInputStream( );
		CymbolLexer lexer = new CymbolLexer(input);
		CommonTokenStream tokens = new CommonTokenStream(lexer);
		CymbolParser parser = new CymbolParser(tokens);
		ParseTree tree = parser.file( );
		
		CymbolCheckerVisitor visitor = new CymbolCheckerVisitor( );
		tree.accept(visitor);
		
		System.out.println("Checagem de tipos encerrada com sucesso!");
	}
}
